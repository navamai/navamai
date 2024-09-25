import os

import click
from rich.console import Console

import navamai.configure as configure
import navamai.markdown as markdown
import navamai.utils as utils

console = Console()


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
