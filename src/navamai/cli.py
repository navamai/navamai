import click
import navamai.utils as utils
from navamai.claude import Claude
from navamai.ollama import Ollama
from navamai.groq import Groq
from navamai.openai import Openai
from navamai.gemini import Gemini
import importlib.resources
from pathlib import Path
import shutil
import os
import re
import io
from difflib import SequenceMatcher

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from rich.table import Table
from rich import box

import tempfile
import shutil
import requests
import mimetypes

from PIL import Image
import cv2

import term_image.image as TermImage
import subprocess

console = Console()

import os
import tempfile

def display_image(image_path):
    if 'TERM_PROGRAM' in os.environ and os.environ['TERM_PROGRAM'] == 'vscode':
        img = TermImage.from_file(image_path)
        img.draw()
    else:
        console.print(f"Browse processed image at: {image_path}")

def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot access the camera")
    
    # Wait for the camera to initialize and adjust light levels
    for i in range(30):
        cap.read()
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret or frame is None:
        raise IOError("Failed to capture an image")
    
    _, buffer = cv2.imencode('.jpg', frame)
    
    return buffer.tobytes()

# [TODO] Resize image based on lowest common denominator for vision models
def resize_image(image_data, max_size=5*1024*1024):
    """Resize the image to ensure it's under 5MB."""
    img = Image.open(io.BytesIO(image_data))
    
    # Calculate current size
    current_size = len(image_data)
    
    if current_size <= max_size:
        return image_data  # No need to resize
    
    # Calculate the scale factor
    scale_factor = (max_size / current_size) ** 0.5
    
    # Calculate new dimensions
    new_width = int(img.width * scale_factor)
    new_height = int(img.height * scale_factor)
    
    # Resize the image
    img_resized = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Convert back to bytes
    buffer = io.BytesIO()
    img_resized.save(buffer, format="JPEG", quality=85)
    return buffer.getvalue()

def extract_error_info(error_message):
    # Extract error code
    error_code_match = re.search(r"Error code: (\d+)", error_message)
    error_code = error_code_match.group(1) if error_code_match else "Unknown"

    # Extract error content
    error_content_match = re.search(r"\{.*\}", error_message)
    if error_content_match:
        error_content = error_content_match.group(0)
    else:
        # If no JSON-like content found, use the last line of the error message
        error_content = error_message.strip().split('\n')[-1]

    return error_code, error_content


@click.group()
def cli():
    pass

@cli.command()
@click.argument('model_config', type=click.Choice(['ask', 'validate', 'intents', 'expand-intents', 'vision']))
def test(model_config):
    """Test the specified model configuration across all compatible providers and models."""
    config = utils.load_config()
    provider_model_mapping = config.get('provider-model-mapping', {})
    
    summary = []

    for provider, models in provider_model_mapping.items():
        for model in models:
            # Update the configuration
            config[model_config]['provider'] = provider            
            config[model_config]['model'] = model

            # Save the updated configuration
            utils.save_config(config)

            # Prepare the command
            if model_config == 'ask':
                cmd = ['navamai', 'ask', 'How old is the oldest pyramid.']
            elif model_config == 'intents':
                cmd = ['navamai', 'intents', 'Financial Analysis']
            elif model_config == 'expand-intents':
                cmd = ['navamai', 'expand-intents', 'Financial Analysis']
            elif model_config == 'validate':
                cmd = ['navamai', 'validate', 'Financial Analysis']
            elif model_config == 'vision':
                if model in config.get('vision-models', []):
                    cmd = ['navamai', 'vision', '-p', 'Images/hackathon.jpg', 'Describe this image.']
                else:
                    console.print(f"Skipping vision test for {provider} - {model} as it's not in the vision-models list.", style="yellow")
                    summary.append({
                        'Provider': provider,
                        'Model': config[model_config]['model'],
                        'Config': model_config,
                        'Status': 'Skipped',
                        'Details': 'Not in vision-models list'
                    })
                    continue

            console.print(f"\nTesting [bold green]{model_config}[/bold green] with [bold blue]{provider}[/bold blue] - [bold magenta]{config[model_config]['model']}[/bold magenta]")
            console.print("-" * 40)

            # Run the command
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                console.print(result.stdout)
                summary.append({
                    'Provider': provider,
                    'Model': config[model_config]['model'],
                    'Config': model_config,
                    'Status': 'Success',
                    'Details': 'Command executed successfully'
                })
            except subprocess.CalledProcessError as e:
                error_code, error_content = extract_error_info(e.stderr)
                console.print(f"Error occurred (Code {error_code}): {error_content}", style="bold red")
                summary.append({
                    'Provider': provider,
                    'Model': config[model_config]['model'],
                    'Config': model_config,
                    'Status': 'Failed',
                    'Details': f"Error {error_code}: {error_content}"
                })
            except Exception as e:
                console.print(f"An unexpected error occurred: {str(e)}", style="bold red")
                summary.append({
                    'Provider': provider,
                    'Model': config[model_config]['model'],
                    'Config': model_config,
                    'Status': 'Error',
                    'Details': str(e)
                })

    console.print("\nTest Summary:", style="bold underline")
    table = Table(title="Test Results", box=box.ROUNDED)
    table.add_column("Provider", style="cyan")
    table.add_column("Model", style="magenta")
    table.add_column("Config", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Details", style="white")

    for entry in summary:
        status_style = "green" if entry['Status'] == 'Success' else "red"
        table.add_row(
            entry['Provider'],
            entry['Model'],
            entry['Config'],
            f"[{status_style}]{entry['Status']}[/{status_style}]",
            entry['Details']
        )

    console.print(table)

    success_count = sum(1 for entry in summary if entry['Status'] == 'Success')
    total_count = len(summary)
    success_rate = (success_count / total_count) * 100 if total_count > 0 else 0

    console.print(f"\nTotal tests: {total_count}")
    console.print(f"Successful tests: {success_count}")
    console.print(f"Success rate: {success_rate:.2f}%")

    console.print("\nTest completed.", style="bold green")

@cli.command()
@click.option('--force', is_flag=True, help='Overwrite existing files without prompting')
def init(force):
    click.echo("Initializing navamai in the current directory...")

    current_dir = Path.cwd()
    copied_files = []
    created_folders = []

    try:
        package = 'navamai'
        scaffold_dir = 'scaffold'

        with importlib.resources.path(package, scaffold_dir) as scaffold_path:
            if not scaffold_path.exists():
                click.echo(f"Scaffold directory '{scaffold_dir}' does not exist in the package.")
                return

            for root, dirs, files in os.walk(scaffold_path):
                rel_path = Path(root).relative_to(scaffold_path)
                target_dir = current_dir / rel_path

                if not target_dir.exists():
                    target_dir.mkdir(parents=True, exist_ok=True)
                    created_folders.append(str(rel_path))

                for file in files:
                    source_file = Path(root) / file
                    target_file = target_dir / file

                    if target_file.exists() and not force:
                        if click.confirm(f"File '{target_file}' already exists. Overwrite?", default=False):
                            shutil.copy2(source_file, target_file)
                            copied_files.append(str(rel_path / file))
                    else:
                        shutil.copy2(source_file, target_file)
                        copied_files.append(str(rel_path / file))

        # Summarize actions
        summary = f"Initialized navamai in {current_dir}"
        if copied_files:
            summary += f"\nCopied files: {', '.join(copied_files)}"
        if created_folders:
            summary += f"\nCreated folders: {', '.join(created_folders)}"
        click.echo(summary)

    except Exception as e:
        click.echo(f"An error occurred during initialization: {e}")

@cli.command()
@click.argument('config_path', nargs=-1)
@click.argument('value')
def config(config_path, value):
    keys = list(config_path)
    utils.edit_config(keys, value)
    click.echo(f"Updated config: {' > '.join(keys)} = {value}")


@cli.command()
@click.option('-i', '--identify', is_flag=True, help='Identify the provider and model without running a query')
@click.argument('prompt', required=False)
def ask(identify, prompt):
    config = utils.load_config()
    ask_config = config.get("ask", {})
    
    provider = ask_config.get("provider").lower()
    provider_instance = _get_provider_instance(provider)
    provider_instance.set_model_config("ask")
    if identify:
        model_info = provider_instance.get_model_info()
        console.print(f"Model Information: [bold magenta]{model_info}[/bold magenta]")
    elif prompt:
        provider_instance.ask(prompt)
    else:
        click.echo("Error: Please provide a prompt or use the --identify flag.")


@cli.command()
@click.argument('template', required=True)
def expand_intents(template):
    config = utils.load_config()
    model_config = config.get("expand-intents", {})
    intents_template = f"{model_config['lookup-folder']}/{template}.md"
    provider = model_config.get("provider").lower()
    provider_instance = _get_provider_instance(provider)
    provider_instance.set_model_config("expand-intents")
    
    with open(intents_template, 'r') as file:
        template_contents = file.read()
    
    provider_instance.ask(prompt=template_contents, title=template)

@cli.command()
@click.argument('filename')
def intents(filename):
    config = utils.load_config()
    model_config = config.get("intents", {})

    intents_template = f"{model_config.get("lookup-folder")}/{filename}.md"

    if not os.path.exists(intents_template):
        click.echo(f"Error: Intents file {intents_template} not found.")
        return

    with open(intents_template, 'r') as file:
        intents_content = file.read()

    sections = _parse_markdown_sections(intents_content)

    for i, (title, _) in enumerate(sections, 1):
        click.echo(f"[{i}] {title}")

    while True:
        choice = click.prompt("Select an option", type=int)
        if 1 <= choice <= len(sections):
            break
        click.echo(f"Invalid choice. Please enter a number between 1 and {len(sections)}.")

    selected_title, selected_prompt = sections[choice - 1]

    # Check if a response file already exists
    response_filename = f"{selected_title}.md"
    response_file_path = os.path.join(model_config.get("save-folder"), response_filename)

    if os.path.exists(response_file_path):
        replace = click.confirm(f"A response file '{response_filename}' already exists. Do you want to replace it?", default=False)
        if not replace:
            click.echo("Operation cancelled. Existing file will not be replaced.")
            return

    click.echo(f"Executing prompt: {selected_prompt}")
    
    provider = model_config.get("provider").lower()

    provider_instance = _get_provider_instance(provider)
    provider_instance.set_model_config("intents")

    # Execute the ask method and capture the response file path
    new_response_file_path = provider_instance.ask(selected_prompt, title=selected_title)

    # Update the Markdown file if a response was saved
    if new_response_file_path:
        _update_markdown_with_response(intents_template, selected_title, os.path.basename(new_response_file_path))
        click.echo(f"Updated {intents_template} with response file path.")

@cli.command()
@click.argument('filename')
def validate(filename):
    config = utils.load_config()
    intents_config = config.get("intents", {})
    validate_config = config.get("validate", {})

    intents_template = f"{intents_config.get('lookup-folder')}/{filename}.md"

    if not os.path.exists(intents_template):
        click.echo(f"Error: Intents file {intents_template} not found.")
        return

    with open(intents_template, 'r') as file:
        intents_content = file.read()

    sections = _parse_markdown_sections(intents_content)

    for i, (title, _) in enumerate(sections, 1):
        click.echo(f"[{i}] {title}")

    while True:
        choice = click.prompt("Select an option", type=int)
        if 1 <= choice <= len(sections):
            break
        click.echo(f"Invalid choice. Please enter a number between 1 and {len(sections)}.")

    selected_title, selected_prompt = sections[choice - 1]

    # Check if a response file already exists
    response_filename = f"{selected_title}.md"
    response_file_path = os.path.join(intents_config.get("save-folder"), response_filename)

    if not os.path.exists(response_file_path):
        click.echo(f"Error: Response file '{response_filename}' not found.")
        return

    with open(response_file_path, 'r') as file:
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

    provider_instance = _get_provider_instance(provider)
    provider_instance.set_model_config("validate")

    # Execute the ask method and capture the validated response
    validated_response_file_path = provider_instance.ask(validation_prompt, title=f"{selected_title} validated")

    if validated_response_file_path:
        with open(validated_response_file_path, 'r') as file:
            validated_response = file.read()

        # Perform text diff
        diff_percentage = _diff(existing_response, validated_response)
        click.echo(f"{diff_percentage:.2f}% validated content is different from original.")
    else:
        click.echo("Validation failed. No changes made to the existing response.")


@cli.command()
@click.option('-p', '--path', type=click.Path(exists=True), help='Path to the local image file')
@click.option('-u', '--url', type=str, help='URL of the online image')
@click.option('-c', '--camera', is_flag=True, help='Capture image from camera')
@click.option('-d', '--display', is_flag=True, help='Display image')
@click.option('-i', '--identify', is_flag=True, help='Identify the provider and model without running a query')
@click.argument('prompt', required=False)
def vision(path, url, camera, identify, display, prompt):
    config = utils.load_config()
    vision_config = config.get("vision", {})

    provider = vision_config.get("provider").lower()
    model = vision_config.get("model")

    provider_instance = _get_provider_instance(provider)
    provider_instance.set_model_config("vision")

    if identify:
        model_info = provider_instance.get_model_info()
        console.print(f"Model Information: [bold magenta]{model_info}[/bold magenta]")
        return
    
    if sum(bool(x) for x in (path, url, camera)) != 1:
        console.print("[bold red]Error:[/bold red] Please provide exactly one of: local image file path (-p), image URL (-u), or camera capture (-c)")
        return

    if not utils.has_vision_capability(model):
        console.print(f"[bold red]Error:[/bold red] The selected model '{model}' does not have vision capabilities.")
        vision_models = config.get("vision-models", [])
        console.print(Panel(f"Please choose one of the following vision-capable models:\n{', '.join(vision_models)}", title="Available Vision Models", border_style="yellow"))
        return

    # Handle image loading
    with console.status("[bold green]Loading image...[/bold green]"):
        if url:
            headers = {
                'User-Agent': 'Navamai/1.0 (https://github.com/navamai/navamai; team@navamai.com) Python/3.12'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            image_data = response.content
            image_source = "URL"
        elif camera:
            image_data = capture_image()
            image_source = "Camera"
        else:
            image_source = path
            with open(image_source, 'rb') as img_file:
                image_data = img_file.read()

    image_data = resize_image(image_data)

    # Create a temporary file to display the image
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(image_data)
        temp_file_path = temp_file.name

    if display:
        display_image(temp_file_path)

    if prompt:
        console.print("[bold green]Processing image and generating response...[/bold green]")

        # Stream the text response
        with Live(console=console, refresh_per_second=8) as live:
            full_response = ""
            for chunk in provider_instance.stream_vision_response(image_data, prompt):
                full_response += chunk
                live.update(Markdown(full_response))

        if vision_config.get("save", False):
            response_file_path = provider_instance.save_response(prompt, full_response)
            
            # Save the original image more efficiently
            image_filename = os.path.splitext(os.path.basename(response_file_path))[0]
            image_path = os.path.join(os.path.dirname(response_file_path), image_filename)
            
            if path:
                # For local files, simply copy the original file
                image_extension = os.path.splitext(path)[1]
                dest_path = f"{image_path}{image_extension}"
                shutil.copy2(path, dest_path)
                console.print(f"[bold green]Original image copied to:[/bold green] {dest_path}")
            elif url:
                # For URLs, download the image directly
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    extension = mimetypes.guess_extension(content_type) or '.jpg'
                    dest_path = f"{image_path}{extension}"
                    with open(dest_path, 'wb') as f:
                        response.raw.decode_content = True
                        shutil.copyfileobj(response.raw, f)
                    console.print(f"[bold green]Image downloaded and saved to:[/bold green] {dest_path}")
                else:
                    console.print("[bold red]Failed to download the image from the URL.[/bold red]")
            elif camera:
                # For camera capture, we still need to save the image_data
                dest_path = f"{image_path}.jpg"
                with open(dest_path, 'wb') as img_file:
                    img_file.write(image_data)
                console.print(f"[bold green]Captured image saved to:[/bold green] {dest_path}")
    else:
        console.print("[bold red]Error:[/bold red] Please provide a prompt or use the --identify flag.")

    # Clean up temporary file
    if os.path.exists(temp_file_path):
        os.unlink(temp_file_path)


def _diff(content1, content2):
    def preprocess_content(content):
        # Remove newlines and extra whitespace
        content = re.sub(r'\s+', ' ', content)
        # Remove all markdown formatting
        content = re.sub(r'[#*_`~\[\]()>]+', '', content)
        # Remove links
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
        # Remove HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        return content.strip().lower()

    # Preprocess both contents
    processed_content1 = preprocess_content(content1)
    processed_content2 = preprocess_content(content2)

    # Calculate similarity ratio
    similarity = SequenceMatcher(None, processed_content1, processed_content2).ratio()

    # Calculate difference percentage
    difference_percentage = (1 - similarity) * 100

    return difference_percentage
def _parse_markdown_sections(content):
    pattern = r'^#\s(.+)\n\nPrompt:\s(.+)$'
    return re.findall(pattern, content, re.MULTILINE)

def _get_provider_instance(provider):
    if provider == "claude":
        return Claude()
    elif provider == "ollama":
        return Ollama()
    elif provider == "groq":
        return Groq()
    elif provider == "openai":
        return Openai()
    elif provider == "gemini":
        return Gemini()
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def _update_markdown_with_response(filename, title, response_filename):
    with open(filename, 'r') as file:
        content = file.read()

    # Create the Obsidian-flavored markdown embed
    embed = f"![[{response_filename}]]"

    # Find the section and check if the embed already exists
    pattern = f"(#\\s{re.escape(title)}.*?^Prompt:.*?$)(.*?)(?=^#|\\Z)"
    match = re.search(pattern, content, flags=re.MULTILINE | re.DOTALL)
    
    if match:
        section_content = match.group(2)
        if embed in section_content:
            # Embed already exists, do nothing
            return
        
        # Embed doesn't exist, add it
        replacement = f"{match.group(1)}\n\n{embed}"
        updated_content = content[:match.start()] + replacement + '\n\n' + content[match.end():]
    else:
        # Section not found, don't modify the file
        return

    with open(filename, 'w') as file:
        file.write(updated_content)

if __name__ == "__main__":
    cli()