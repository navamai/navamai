import navamai.configure as configure
from rich.console import Console
import navamai.markdown as markdown
import os
import sys
import click
import navamai.utils as utils


console = Console()

def process(document):
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
