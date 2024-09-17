import importlib.resources
import mimetypes
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional

import click
import requests
from rich import box
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

import navamai.auditor as auditor
import navamai.configure as configure
import navamai.images as images
import navamai.markdown as markdown
import navamai.metrics as metrics
import navamai.utils as utils
from navamai.utils import trail
import navamai.gather as gather_utils
import navamai.code as code

console = Console()


@click.group()
def cli():
    pass

@cli.command()
def run():
    config = configure.load_config()
    run_config = config.get("run")
    lookup_folder = run_config.get("lookup-folder")
    save_folder = run_config.get("save-folder")
    selected_file = markdown.file_select_paginate(lookup_folder)
    if not selected_file:
        console.print("[yellow]No file selected. Exiting.[/yellow]")
        sys.exit(0)
    else:
        code.process_markdown_file(selected_file, app_folder=save_folder)

@cli.command()
def audit():
    auditor.trail_auditor("trail.yml")

@cli.command()
@click.argument("type", required=True)
@click.argument("url", required=True)
def gather(type, url):
    if type == "article":
        gather_utils.article(url)
    else:
        console.print(f"Invalid type: {type}", style="red")


@cli.command()
@click.argument("filepath", required=True)
def split(filepath):
    markdown.split_text_by_tokens(filepath)


@cli.command()
@click.option("-d", "--days", default=7, help="Number of days to analyze")
def trends(days):
    """Visualize trends for provider-model combinations."""
    data = metrics.read_yaml_files()
    processed_data = metrics.process_data(data, days)
    metrics.display_trends(processed_data)


@cli.command()
@click.argument("model_config", type=click.Choice(["ask", "vision"]))
def test(model_config):
    """Test the specified model configuration across all compatible providers and models."""
    config = configure.load_config()
    provider_model_mapping = config.get("provider-model-mapping", {})
    test_config = config.get("test", {})

    # Store original configuration
    original_provider = config[model_config]["provider"]
    original_model = config[model_config]["model"]

    summary = []

    try:
        for provider, models in provider_model_mapping.items():
            for model in models:
                # Update the configuration
                config[model_config]["provider"] = provider
                config[model_config]["model"] = model

                # Save the updated configuration
                configure.save_config(config)

                # Get the prompt from the config file
                if model_config == "ask":
                    prompt = test_config.get("ask")
                elif model_config == "vision":
                    prompt = test_config.get("vision")

                media_type = None
                if model_config == "vision":
                    if model in config.get("vision-models", []):
                        image_path = test_config.get("image-path")
                        # set media_type based on the image extension
                        extension = os.path.splitext(image_path)[1]
                        media_type = mimetypes.types_map.get(extension, "image/jpeg")
                    else:
                        console.print(
                            f"Skipping vision test for {provider} - {model} as it's not in the vision-models list.",
                            style="yellow",
                        )
                        summary.append(
                            {
                                "Provider": provider,
                                "Model": config[model_config]["model"],
                                "Config": model_config,
                                "Status": "Skipped",
                                "Details": "Not in vision-models list",
                                "Response Time": float(
                                    "inf"
                                ),  # Use infinity for sorting purposes
                                "Token Count": "N/A",
                            }
                        )
                        continue

                console.print(
                    f"\nTesting [bold green]{model_config}[/bold green] with [bold blue]{provider}[/bold blue] - [bold magenta]{config[model_config]['model']}[/bold magenta]"
                )
                console.print(f"Prompt: [italic]{prompt}[/italic]")
                console.print("-" * 40)

                # Run the command
                try:
                    provider_instance = utils.get_provider_instance(provider)
                    provider_instance.set_model_config(model_config)

                    start_time = time.time()
                    with Live(console=console, refresh_per_second=8) as live:
                        full_response = ""
                        if model_config == "vision":
                            with open(image_path, "rb") as img_file:
                                image_data = img_file.read()
                            for chunk in provider_instance.stream_vision_response(
                                image_data, prompt, media_type
                            ):
                                full_response += chunk
                                live.update(Markdown(full_response))
                        else:
                            for chunk in provider_instance.stream_response(prompt):
                                full_response += chunk
                                live.update(Markdown(full_response))
                    end_time = time.time()

                    response_time = end_time - start_time
                    token_count = metrics.count_tokens(full_response)

                    summary.append(
                        {
                            "Provider": provider,
                            "Model": config[model_config]["model"],
                            "Config": model_config,
                            "Status": "Success",
                            "Details": "Command executed successfully",
                            "Response Time": response_time,
                            "Token Count": token_count,
                        }
                    )

                    # NEW: Save test summary to YAML
                    metrics.save_test_summary(
                        provider,
                        config[model_config]["model"],
                        model_config,
                        prompt,
                        "Success",
                        "Command executed successfully",
                        response_time,
                        token_count,
                    )

                except Exception as e:
                    error_message = str(e)
                    console.print(f"An error occurred: {error_message}", style="bold red")
                    summary.append(
                        {
                            "Provider": provider,
                            "Model": config[model_config]["model"],
                            "Config": model_config,
                            "Status": "Error",
                            "Details": error_message,
                            "Response Time": float(
                                "inf"
                            ),  # Use infinity for sorting purposes
                            "Token Count": "N/A",
                        }
                    )

                    # NEW: Save error summary to YAML
                    metrics.save_test_summary(
                        provider,
                        config[model_config]["model"],
                        model_config,
                        prompt,
                        "Error",
                        error_message,
                        float("inf"),
                        "N/A",
                    )

    finally:
        # Revert to the original configuration
        config[model_config]["provider"] = original_provider
        config[model_config]["model"] = original_model
        configure.save_config(config)

    # Sort summary by response time
    summary.sort(key=lambda x: x["Response Time"])

    console.print("\nTest Summary:", style="bold underline")
    table = Table(title="Test Results (Sorted by Response Time)", box=box.ROUNDED)
    table.add_column("Provider", style="cyan")
    table.add_column("Model", style="magenta")
    table.add_column("Config", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Details", style="white")
    table.add_column("Response Time", style="cyan")
    table.add_column("Token Count", style="orange3")

    for entry in summary:
        status_style = "green" if entry["Status"] == "Success" else "red"
        response_time = (
            f"{entry['Response Time']:.2f}s"
            if isinstance(entry['Response Time'], float)
            and entry['Response Time'] != float("inf")
            else "N/A"
        )
        table.add_row(
            entry["Provider"],
            entry["Model"],
            entry["Config"],
            f"[{status_style}]{entry['Status']}[/{status_style}]",
            entry["Details"],
            response_time,
            str(entry["Token Count"]),
        )

    console.print(table)

    success_count = sum(1 for entry in summary if entry["Status"] == "Success")
    total_count = len(summary)
    success_rate = (success_count / total_count) * 100 if total_count > 0 else 0

    console.print(f"\nTotal tests: {total_count}")
    console.print(f"Successful tests: {success_count}")
    console.print(f"Success rate: {success_rate:.2f}%")

    console.print("\nTest completed.", style="bold green")


@cli.command()
@click.option(
    "-f", "--force", is_flag=True, help="Overwrite existing files without prompting"
)
def init(force):
    click.echo("Initializing navamai in the current directory...")

    current_dir = Path.cwd()
    copied_files = []

    try:
        package = "navamai"
        scaffold_dir = "scaffold"

        console.print(f"Copying scaffold files from {package}...", style="green")
        with importlib.resources.path(package, scaffold_dir) as scaffold_path:
            if not scaffold_path.exists():
                click.echo(
                    f"Scaffold directory '{scaffold_dir}' does not exist in the package."
                )
                return

            for root, dirs, files in os.walk(scaffold_path):
                rel_path = Path(root).relative_to(scaffold_path)
                target_dir = current_dir / rel_path

                if not target_dir.exists():
                    target_dir.mkdir(parents=True, exist_ok=True)
                    console.print(f"Created folder {target_dir}", style="bold cyan")

                for file in files:
                    source_file = Path(root) / file
                    target_file = target_dir / file

                    if target_file.exists() and not force:
                        if click.confirm(
                            f"File '{target_file}' already exists. Overwrite?",
                            default=False,
                        ):
                            shutil.copy2(source_file, target_file)
                            copied_files.append(str(rel_path / file))
                    else:
                        shutil.copy2(source_file, target_file)
                        console.print(f"Copied {file} to {target_dir}", style="cyan")

        console.print(f"Initialized navamai in {current_dir}", style="bold green")

    except Exception as e:
        click.echo(f"An error occurred during initialization: {e}")


@cli.command()
@click.argument("config_path", nargs=-1)
@click.argument("value")
def config(config_path, value):
    keys = list(config_path)
    configure.edit_config(keys, value)
    click.echo(f"Updated config: {' > '.join(keys)} = {value}")


@cli.command()
@click.argument("section", required=False)
def id(section):
    section = "ask" if section is None else section
    config = configure.load_config()
    model_config = config.get(section)

    provider = model_config.get("provider").lower()
    provider_instance = utils.get_provider_instance(provider)
    provider_instance.set_model_config(section)

    model_info = provider_instance.get_model_info()
    console.print(f"Model Information: [bold magenta]{model_info}[/bold magenta]")
    sys.exit(0)


@cli.command()
@click.argument("prompt", required=False)
@click.argument("template", required=False)
@trail
def ask(prompt, template):
    config = configure.load_config()
    model_config = config.get("ask", {})

    provider = model_config.get("provider").lower()
    provider_instance = utils.get_provider_instance(provider)
    provider_instance.set_model_config("ask")
    destination_file = None
    selected_file = None
    template_prompt = None

    if prompt:
        destination_file = provider_instance.ask(prompt)
    elif template:
        with open(template, "r") as f:
            template_prompt = f.read().strip()

        prompt_variables = markdown.extract_variables(prompt)

        # check if the prompt has variables. If so, ask for values
        if prompt_variables:
            console.print(
                "The Prompt Template has variables. Enter values for the following variables:",
                style="yellow",
            )
            for variable in prompt_variables:
                value = click.prompt(variable)
                template_prompt = template_prompt.replace(variable, value)

        destination_file = provider_instance.ask(template_prompt)
    else:
        prompts_dir = model_config.get("prompts-folder")
        if not os.path.exists(prompts_dir):
            console.print(
                f"[bold red]Error:[/bold red] Prompts directory not found at {prompts_dir}"
            )
            sys.exit(1)

        selected_file = markdown.file_select_paginate(prompts_dir)
        if selected_file:
            with open(selected_file, "r") as f:
                template_prompt = f.read().strip()

            prompt_variables = markdown.extract_variables(template_prompt)

            # check if the prompt has variables. If so, ask for values
            if prompt_variables:
                console.print(
                    "The Prompt Template has variables. Please enter values.",
                    style="yellow",
                )
                for variable in prompt_variables:
                    if variable == "TEXT_FILE":
                        console.print(
                            "TEXT_FILE:",
                            style="yellow",
                        )
                        # open the file and read the contents into value
                        variable_file = markdown.file_select_paginate(
                            model_config.get("lookup-folder")
                        )

                        if not variable_file:
                            console.print("[yellow]No file selected. Exiting.[/yellow]")
                            sys.exit(0)

                        with open(variable_file, "r") as f:
                            value = f.read()

                        template_prompt = template_prompt.replace(variable, value)
                    else:
                        value = click.prompt(variable)
                        template_prompt = template_prompt.replace(variable, value)

            destination_file = provider_instance.ask(template_prompt)
        else:
            console.print("[yellow]No file selected. Exiting.[/yellow]")
            sys.exit(0)

    if not prompt and not template_prompt:
        console.print("[bold red]Error:[/bold red] No prompt provided")
        sys.exit(1)

    return {
        "custom_prompt": prompt,
        "prompt_file": selected_file,
        "destination_file": destination_file,
    }


def document_prompt(
    config_section: str, document: Optional[str] = None, prompt: Optional[str] = None
):
    config = configure.load_config()
    model_config = config.get(f"{config_section}")
    lookup_folder = model_config["lookup-folder"]

    if not document:
        document = markdown.file_select_paginate(
            lookup_folder, show_tokens=True, section=config_section
        )

    if not document:
        console.print("[yellow]No file selected. Exiting.[/yellow]")
        sys.exit(0)

    source_document = document
    file_name = os.path.basename(source_document).replace(".md", "")

    if not os.path.exists(source_document):
        raise click.ClickException(
            f"Document '{source_document}' not found in {lookup_folder}"
        )

    provider = model_config.get("provider").lower()
    provider_instance = utils.get_provider_instance(provider)
    provider_instance.set_model_config(f"{config_section}")

    custom_prompt = None
    with open(source_document, "r") as file:
        source_contents = file.read()

    if prompt:
        destination_file = provider_instance.ask(
            prompt=f"{prompt}\n\n{source_contents}", title=f"{document} updated"
        )
    else:
        console.print(
            f"Using system prompt: {model_config.get('system')}", style="cyan"
        )
        add_custom_prompt = click.confirm(
            "Do you want to add a custom prompt?", default=True
        )
        if add_custom_prompt:
            custom_prompt = click.prompt("Enter a custom prompt")
            destination_file = provider_instance.ask(
                prompt=f"{custom_prompt}\n\n{source_contents}",
                title=f"{file_name} updated",
            )
        else:
            destination_file = provider_instance.ask(
                prompt=source_contents, title=f"{file_name} updated"
            )
    return source_document, destination_file, custom_prompt


@cli.command()
@click.argument("section", required=True)
@click.option("-d", "--document", help="The document to refer")
@click.option(
    "-p", "--prompt", help="Additional prompt to use when referring the document"
)
@trail
def refer(section: str, document: Optional[str] = None, prompt: Optional[str] = None):
    source_document, destination_file, custom_prompt = document_prompt(
        config_section=f"refer-{section}", document=document, prompt=prompt
    )
    return {
        "custom_prompt": custom_prompt,
        "source_file": source_document,
        "destination_file": destination_file,
    }


@cli.command()
@click.option("-d", "--document", help="Filename of the document to process")
@trail
def intents(document):
    config = configure.load_config()
    model_config = config.get("intents", {})
    lookup_folder = model_config.get("lookup-folder")

    if not document:
        console.print("Select from available documents...", style="green")
        document = markdown.file_select_paginate(lookup_folder)

    if not document:
        console.print("[yellow]No file selected. Exiting.[/yellow]")
        sys.exit(0)

    intents_template = document

    with open(intents_template, "r") as file:
        intents_content = file.read()

    sections = markdown.parse_markdown_sections(intents_content)
    console.print("Select from available intents to generate embed...", style="green")

    selected_intent = markdown.intent_select_paginate(sections)

    if selected_intent:
        selected_title, selected_prompt = selected_intent
    else:
        console.print("No intent selected. Exiting.")
        return

    # Check if a response file already exists
    response_filename = f"{selected_title}.md"
    response_file_path = os.path.join(
        model_config.get("save-folder"), response_filename
    )

    if os.path.exists(response_file_path):
        replace = click.confirm(
            f"A response file '{response_filename}' already exists. Do you want to replace it?",
            default=False,
        )
        if not replace:
            click.echo("Operation cancelled. Existing file will not be replaced.")
            return

    click.echo(f"Executing prompt: {selected_prompt}")

    provider = model_config.get("provider").lower()

    provider_instance = utils.get_provider_instance(provider)
    provider_instance.set_model_config("intents")

    # Execute the ask method and capture the response file path
    new_response_file_path = provider_instance.ask(
        selected_prompt, title=selected_title
    )

    # Update the Markdown file if a response was saved
    if new_response_file_path:
        markdown.update_markdown_with_response(
            intents_template, selected_title, os.path.basename(new_response_file_path)
        )
        click.echo(f"Updated {intents_template} with response file path.")
    return {"source_file": intents_template, "destination_file": new_response_file_path}


@cli.command()
@click.argument("filename")
def merge(filename):
    config = configure.load_config()
    merge_config = config.get("merge", {})
    markdown.merge_docs(
        source_path=f"{merge_config.get('lookup-folder')}/{filename}",
        dest_suffix=merge_config.get("dest-suffix"),
        merge_suffix=merge_config.get("merge-suffix"),
        placeholder=merge_config.get("placeholder"),
        prompt_prefix=merge_config.get("prompt-prefix"),
    )


@cli.command()
@click.option("-d", "--document", help="Filename of the document to process")
@trail
def validate(document):
    config = configure.load_config()
    validate_config = config.get("validate", {})
    lookup_folder = validate_config.get("lookup-folder")

    if not document:
        console.print("Select from available documents...", style="green")
        # List documents in lookup-folder
        documents = [
            f.replace(".md", "") for f in os.listdir(lookup_folder) if f.endswith(".md")
        ]
        for i, doc in enumerate(documents, 1):
            click.echo(f"[{i}] {doc}")

        while True:
            choice = click.prompt("Select a document", type=int)
            if 1 <= choice <= len(documents):
                document = documents[choice - 1]
                break
            click.echo(
                f"Invalid choice. Please enter a number between 1 and {len(documents)}."
            )

    intents_template = os.path.join(lookup_folder, f"{document}.md")

    if not os.path.exists(intents_template):
        click.echo(f"Error: Intents file {intents_template} not found.")
        return

    with open(intents_template, "r") as file:
        intents_content = file.read()

    sections = markdown.parse_markdown_sections(intents_content)

    for i, (title, _) in enumerate(sections, 1):
        click.echo(f"[{i}] {title}")

    while True:
        choice = click.prompt("Select an option", type=int)
        if 1 <= choice <= len(sections):
            break
        click.echo(
            f"Invalid choice. Please enter a number between 1 and {len(sections)}."
        )

    selected_title, selected_prompt = sections[choice - 1]

    # Check if a response file already exists
    response_filename = f"{selected_title}.md"
    response_file_path = os.path.join(
        validate_config.get("save-folder"), response_filename
    )

    if not os.path.exists(response_file_path):
        click.echo(f"Error: Response file '{response_filename}' not found.")
        return

    with open(response_file_path, "r") as file:
        existing_response = file.read()

    validate_prompt = validate_config.get("validate-prompt")
    # Create the validation prompt
    validation_prompt = (
        f"{validate_prompt}\n\n"
        f"Prompt: {selected_prompt}\n\n"
        f"Response: {existing_response}"
    )

    click.echo("Validating the response...")

    provider = validate_config.get("provider").lower()

    provider_instance = utils.get_provider_instance(provider)
    provider_instance.set_model_config("validate")

    # Execute the ask method and capture the validated response
    validated_response_file_path = provider_instance.ask(
        validation_prompt, title=f"{selected_title} validated"
    )

    if validated_response_file_path:
        with open(validated_response_file_path, "r") as file:
            validated_response = file.read()

        # Perform text diff
        diff_percentage = markdown.diff(existing_response, validated_response)
        click.echo(
            f"{diff_percentage:.2f}% validated content is different from original."
        )
    else:
        click.echo("Validation failed. No changes made to the existing response.")

    return {
        "source_file": intents_template,
        "destination_file": validated_response_file_path,
    }


@cli.command()
@click.option(
    "-p", "--path", type=click.Path(exists=True), help="Path to the local image file"
)
@click.option("-u", "--url", type=str, help="URL of the online image")
@click.option("-c", "--camera", is_flag=True, help="Capture image from camera")
@click.option("-d", "--display", is_flag=True, help="Display image")
@click.argument("prompt", required=False)
@trail
def vision(path, url, camera, display, prompt):
    config = configure.load_config()
    vision_config = config.get("vision", {})

    provider = vision_config.get("provider").lower()
    model = vision_config.get("model")

    provider_instance = utils.get_provider_instance(provider)
    provider_instance.set_model_config("vision")
    lookup_folder = vision_config.get("lookup-folder")

    if sum(bool(x) for x in (path, url, camera)) != 1:
        path = markdown.file_select_paginate(lookup_folder)
        if not path:
            console.print("[yellow]No file selected. Exiting.[/yellow]")
            sys.exit(0)
        extension = os.path.splitext(path)[1]
        media_type = mimetypes.types_map.get(extension, "image/jpeg")
        if not prompt:
            console.print(
                f"Using system prompt: {vision_config.get('system')}", style="cyan"
            )
            prompt = click.prompt("Enter a custom prompt")

    if not configure.has_vision_capability(model):
        console.print(
            f"[bold red]Error:[/bold red] The selected model '{model}' does not have vision capabilities."
        )
        vision_models = config.get("vision-models", [])
        console.print(
            Panel(
                f"Please choose one of the following vision-capable models:\n{', '.join(vision_models)}",
                title="Available Vision Models",
                border_style="yellow",
            )
        )
        return

    # Handle image loading
    with console.status("[bold green]Loading image...[/bold green]"):
        if url:
            # set media_type based on the image extension
            extension = os.path.splitext(url)[1]
            media_type = mimetypes.types_map.get(extension, "image/jpeg")
            headers = {
                "User-Agent": "Navamai/1.0 (https://github.com/navamai/navamai; team@navamai.com) Python/3.12"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            image_data = response.content
            image_source = "URL"
        elif camera:
            media_type = "image/jpeg"
            image_data = images.capture_image()
            image_source = "Camera"
        else:
            image_source = path
            extension = os.path.splitext(path)[1]
            media_type = mimetypes.types_map.get(extension, "image/jpeg")
            with open(image_source, "rb") as img_file:
                image_data = img_file.read()

    image_data = images.resize_image(image_data)
    dest_path = None

    # Create a temporary file to display the image
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(image_data)
        temp_file_path = temp_file.name

    if display:
        images.display_image(temp_file_path)

    if prompt:
        console.print(
            "[bold green]Processing image and generating response...[/bold green]"
        )

        # Stream the text response
        with Live(console=console, refresh_per_second=8) as live:
            full_response = ""
            for chunk in provider_instance.stream_vision_response(
                image_data, prompt, media_type
            ):
                full_response += chunk
                live.update(Markdown(full_response))

        if vision_config.get("save", False) and full_response:
            response_file_path = provider_instance.save_response(prompt, full_response)

            # Save the original image more efficiently
            image_filename = os.path.splitext(os.path.basename(response_file_path))[0]
            image_path = os.path.join(
                os.path.dirname(response_file_path), image_filename
            )

            if path:
                # For local files, simply copy the original file
                image_extension = os.path.splitext(path)[1]
                dest_path = f"{image_path}{image_extension}"
                shutil.copy2(path, dest_path)
                console.print(
                    f"[bold green]Original image copied to:[/bold green] {dest_path}"
                )
            elif url:
                # For URLs, download the image directly
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    content_type = response.headers.get("content-type", "")
                    extension = mimetypes.guess_extension(content_type) or ".jpg"
                    dest_path = f"{image_path}{extension}"
                    with open(dest_path, "wb") as f:
                        response.raw.decode_content = True
                        shutil.copyfileobj(response.raw, f)
                    console.print(
                        f"[bold green]Image downloaded and saved to:[/bold green] {dest_path}"
                    )
                else:
                    console.print(
                        "[bold red]Failed to download the image from the URL.[/bold red]"
                    )
            elif camera:
                # For camera capture, we still need to save the image_data
                dest_path = f"{image_path}.jpg"
                with open(dest_path, "wb") as img_file:
                    img_file.write(image_data)
                console.print(
                    f"[bold green]Captured image saved to:[/bold green] {dest_path}"
                )
    else:
        console.print(
            "[bold red]Error:[/bold red] Please provide a prompt or use the --identify flag."
        )

    # Clean up temporary file
    if os.path.exists(temp_file_path):
        os.unlink(temp_file_path)

    return {"source_file": image_source, "destination_file": dest_path}


if __name__ == "__main__":
    cli()
