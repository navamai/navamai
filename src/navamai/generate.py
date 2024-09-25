import os
import sys
import threading
import time

import click
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

import navamai.configure as configure
from navamai import markdown, utils

console = Console()


def image(prompt, template):
    config = configure.load_config()
    image_config = config.get("image", {})
    generation_seconds = image_config.get("generation-seconds", 30)

    provider = image_config.get("provider").lower()
    provider_instance = utils.get_provider_instance(provider)
    provider_instance.set_model_config("image")
    destination_file = None
    selected_file = None
    template_prompt = None

    if prompt:
        destination_file = _generate_image_with_progress(
            provider_instance, prompt, generation_seconds
        )
    elif template:
        with open(template, "r") as f:
            template_prompt = f.read().strip()

        prompt_variables = markdown.extract_variables(template_prompt)

        if prompt_variables:
            console = Console()
            console.print(
                "The Prompt Template has variables. Enter values for the following variables:",
                style="yellow",
            )
            for variable in prompt_variables:
                value = click.prompt(variable)
                template_prompt = template_prompt.replace(variable, value)
        destination_file = _generate_image_with_progress(
            provider_instance, template_prompt, generation_seconds
        )
    else:
        prompts_dir = image_config.get("lookup-folder")
        if not os.path.exists(prompts_dir):
            console = Console()
            console.print(
                f"[bold red]Error:[/bold red] Prompts directory not found at {prompts_dir}"
            )
            sys.exit(1)

        selected_file = markdown.file_select_paginate(prompts_dir)
        if selected_file:
            with open(selected_file, "r") as f:
                template_prompt = f.read().strip()

            prompt_variables = markdown.extract_variables(template_prompt)

            if prompt_variables:
                console = Console()
                console.print(
                    "The Prompt Template has variables. Please enter values.",
                    style="yellow",
                )
                for variable in prompt_variables:
                    value = click.prompt(variable)
                    template_prompt = template_prompt.replace(
                        "{{" + variable + "}}", value
                    )
            destination_file = _generate_image_with_progress(
                provider_instance, template_prompt, generation_seconds
            )
        else:
            console = Console()
            console.print("[yellow]No file selected. Exiting.[/yellow]")
            sys.exit(0)

    if not prompt and not template_prompt:
        console = Console()
        console.print("[bold red]Error:[/bold red] No prompt provided")
        sys.exit(1)

    return {
        "custom_prompt": prompt,
        "prompt_file": selected_file,
        "destination_file": destination_file,
    }


def _show_progress(duration, stop_event, progress_complete):
    console = Console()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Generating image in {duration}s", total=duration)
        for remaining in range(duration, 0, -1):
            if stop_event.is_set():
                break
            progress.update(
                task, advance=1, description=f"Generating image in {remaining}s"
            )
            time.sleep(1)

        if not stop_event.is_set():
            progress.update(task, completed=duration)
            progress_complete.set()


def _generate_image_with_progress(provider_instance, prompt, duration):
    stop_event = threading.Event()
    progress_complete = threading.Event()
    progress_thread = threading.Thread(
        target=_show_progress, args=(duration, stop_event, progress_complete)
    )
    progress_thread.start()

    try:
        destination_file = provider_instance.generate_image(prompt)
    finally:
        stop_event.set()
        progress_thread.join()

    console = Console()
    if progress_complete.is_set():
        console.print(f"\nImage saved: {destination_file}", style="green")
    else:
        console.print(
            f"\nImage generated sooner and saved: {destination_file}", style="green"
        )

    return destination_file
