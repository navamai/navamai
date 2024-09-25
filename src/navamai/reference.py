import os
import sys
from typing import Optional

import click
from rich.console import Console

import navamai.configure as configure
import navamai.markdown as markdown
import navamai.utils as utils

console = Console()


def process(section: str, document: Optional[str] = None, prompt: Optional[str] = None):
    source_document, destination_file, custom_prompt = _document_prompt(
        config_section=f"refer-{section}", document=document, prompt=prompt
    )
    return {
        "custom_prompt": custom_prompt,
        "source_file": source_document,
        "destination_file": destination_file,
    }


def _document_prompt(
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
