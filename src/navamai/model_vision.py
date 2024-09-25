import mimetypes
import os
import shutil
import sys
import tempfile

import click
import requests
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel

import navamai.configure as configure
import navamai.images as images
import navamai.markdown as markdown
import navamai.utils as utils

console = Console()


def process(path, url, camera, display, prompt):
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
