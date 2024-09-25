import os
import sys

import click
from rich.console import Console

import navamai.configure as configure
import navamai.markdown as markdown
import navamai.utils as utils

console = Console()


def process(prompt, template):
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
