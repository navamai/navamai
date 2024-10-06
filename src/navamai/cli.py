# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import importlib.resources
import os
import shutil
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console

import navamai.action_intents as action_intents
import navamai.auditor as auditor
import navamai.code as code
import navamai.configure as configure
import navamai.evaluate as evaluate
import navamai.gather as gather_utils
import navamai.generate as generate
import navamai.markdown as markdown
import navamai.metrics as metrics
import navamai.model_text as model_text
import navamai.model_vision as model_vision
import navamai.reference as reference
import navamai.utils as utils
import navamai.validation as validation
from navamai.utils import trail

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
    evaluate.by_model_config(model_config)


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


@click.command()
@click.argument("prompt", required=False)
@click.option("-t", "--template", help="Path to a prompt template file")
def image(prompt, template):
    generate.image(prompt, template)


@cli.command()
@click.argument("prompt", required=False)
@click.argument("template", required=False)
@trail
def ask(prompt, template):
    model_text.process(prompt, template)


@cli.command()
@click.argument("section", required=True)
@click.option("-d", "--document", help="The document to refer")
@click.option(
    "-p", "--prompt", help="Additional prompt to use when referring the document"
)
@trail
def refer(section: str, document: Optional[str] = None, prompt: Optional[str] = None):
    reference.process(section, document, prompt)


@cli.command()
@click.option("-d", "--document", help="Filename of the document to process")
@trail
def intents(document):
    action_intents.process(document)


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
    validation.validate(document)


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
    model_vision.process(path, url, camera, display, prompt)


if __name__ == "__main__":
    cli()
