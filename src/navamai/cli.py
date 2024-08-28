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

@click.group()
def cli():
    pass

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
        click.echo(f"Provider and Model: {model_info}")
    elif prompt:
        provider_instance.ask(prompt)
    else:
        click.echo("Error: Please provide a prompt or use the --identify flag.")


@cli.command()
@click.argument('template', required=True)
def expand_intents(template):
    config = utils.load_config()
    model_config = config.get("expand-intents", {})
    intents_template = f"{model_config['folder']}/{template}.md"
    provider = model_config.get("provider").lower()
    provider_instance = _get_provider_instance(provider)
    provider_instance.set_model_config("expand-intents")
    
    with open(intents_template, 'r') as file:
        template_contents = file.read()
    
    provider_instance.ask(prompt=template_contents, title=template)

@cli.command()
@click.argument('filename')
def intents(filename):
    md_filename = f"Intents/{filename}.md"

    if not os.path.exists(md_filename):
        click.echo(f"Error: Intents file {md_filename} not found.")
        return

    with open(md_filename, 'r') as file:
        md_content = file.read()

    sections = _parse_markdown_sections(md_content)

    for i, (title, _) in enumerate(sections, 1):
        click.echo(f"[{i}] {title}")

    while True:
        choice = click.prompt("Select an option", type=int)
        if 1 <= choice <= len(sections):
            break
        click.echo(f"Invalid choice. Please enter a number between 1 and {len(sections)}.")

    selected_title, selected_prompt = sections[choice - 1]

    config = utils.load_config()
    model_config = config.get("intents", {})

    # Check if a response file already exists
    response_filename = f"{selected_title}.md"
    response_file_path = os.path.join(model_config.get("folder"), response_filename)

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
        _update_markdown_with_response(md_filename, selected_title, os.path.basename(new_response_file_path))
        click.echo(f"Updated {md_filename} with response file path.")

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