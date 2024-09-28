import os
import sys
import click
from rich.console import Console

import navamai.configure as configure
import navamai.markdown as markdown
import navamai.utils as utils

console = Console()


def load_config_and_select_document(lookup_folder):
    config = configure.load_config()
    model_config = config.get("intents", {})

    if not lookup_folder:
        lookup_folder = model_config.get("lookup-folder")

    document = markdown.file_select_paginate(lookup_folder)
    if not document:
        console.print("[yellow]No file selected. Exiting.[/yellow]")
        sys.exit(0)

    return model_config, document


def select_intent(intents_content):
    sections = markdown.parse_markdown_sections(intents_content)
    console.print("Select from available intents to generate embed...", style="green")
    return markdown.intent_select_paginate(sections)


def handle_existing_file(file_path):
    if os.path.exists(file_path):
        return click.confirm(
            f"A response file '{os.path.basename(file_path)}' already exists. Do you want to replace it?",
            default=False,
        )
    return True


def execute_prompt(provider_instance, prompt, title):
    click.echo(f"Executing prompt: {prompt}")
    return provider_instance.ask(prompt, title=title)


def update_markdown(template_file, title, response_file):
    markdown.update_markdown_with_response(
        template_file, title, os.path.basename(response_file)
    )
    click.echo(f"Updated {template_file} with response file path.")


def process(document=None):
    model_config, intents_template = load_config_and_select_document(document)

    with open(intents_template, "r") as file:
        intents_content = file.read()

    selected_intent = select_intent(intents_content)
    if not selected_intent:
        console.print("No intent selected. Exiting.")
        return

    selected_title, selected_prompt = selected_intent
    response_file_path = os.path.join(
        model_config.get("save-folder"), f"{selected_title}.md"
    )

    if not handle_existing_file(response_file_path):
        click.echo("Operation cancelled. Existing file will not be replaced.")
        return

    provider = utils.get_provider_instance(model_config.get("provider").lower())
    provider.set_model_config("intents")

    new_response_file_path = execute_prompt(provider, selected_prompt, selected_title)

    if new_response_file_path:
        update_markdown(intents_template, selected_title, new_response_file_path)

    return {"source_file": intents_template, "destination_file": new_response_file_path}


if __name__ == "__main__":
    process()
