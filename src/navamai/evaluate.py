import mimetypes
import os
import time

from rich import box
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.table import Table

import navamai.configure as configure
from navamai import metrics, utils

console = Console()


def by_model_config(model_config):
    """Evaluate the specified model configuration across all compatible providers and models."""
    config = configure.load_config()
    provider_model_mapping = config.get("provider-model-mapping", {})
    test_config = config.get("test", {})
    image_models = config.get("image-models", [])  # Get the list of image models

    # Store original configuration
    original_provider = config[model_config]["provider"]
    original_model = config[model_config]["model"]

    summary = []

    try:
        for provider, models in provider_model_mapping.items():
            for model in models:
                # Skip image models when running 'ask' test
                if model_config == "ask" and model in image_models:
                    console.print(
                        f"Skipping {provider} - {model} as it's in the image-models list.",
                        style="yellow",
                    )
                    continue

                # Update the configuration
                config[model_config]["provider"] = provider
                config[model_config]["model"] = model

                # Save the updated configuration
                configure.save_config(config)

                # Get the prompt from the config file
                if model_config == "ask":
                    prompt = test_config.get("ask")
                elif model_config == "vision":
                    prompt = test_config.get("vision")

                media_type = None
                if model_config == "vision":
                    if model in config.get("vision-models", []):
                        image_path = test_config.get("image-path")
                        # set media_type based on the image extension
                        extension = os.path.splitext(image_path)[1]
                        media_type = mimetypes.types_map.get(extension, "image/jpeg")
                    else:
                        console.print(
                            f"Skipping vision test for {provider} - {model} as it's not in the vision-models list.",
                            style="yellow",
                        )
                        summary.append(
                            {
                                "Provider": provider,
                                "Model": config[model_config]["model"],
                                "Config": model_config,
                                "Status": "Skipped",
                                "Details": "Not in vision-models list",
                                "Response Time": float("inf"),
                                "Token Count": "N/A",
                            }
                        )
                        continue

                console.print(
                    f"\nTesting [bold green]{model_config}[/bold green] with [bold blue]{provider}[/bold blue] - [bold magenta]{config[model_config]['model']}[/bold magenta]"
                )
                console.print(f"Prompt: [italic]{prompt}[/italic]")
                console.print("-" * 40)

                # Run the command
                try:
                    provider_instance = utils.get_provider_instance(provider)
                    provider_instance.set_model_config(model_config)

                    start_time = time.time()
                    with Live(console=console, refresh_per_second=8) as live:
                        full_response = ""
                        if model_config == "vision":
                            with open(image_path, "rb") as img_file:
                                image_data = img_file.read()
                            for chunk in provider_instance.stream_vision_response(
                                image_data, prompt, media_type
                            ):
                                full_response += chunk
                                live.update(Markdown(full_response))
                        else:
                            for chunk in provider_instance.stream_response(prompt):
                                full_response += chunk
                                live.update(Markdown(full_response))
                    end_time = time.time()

                    response_time = end_time - start_time
                    token_count = metrics.count_tokens(full_response)

                    summary.append(
                        {
                            "Provider": provider,
                            "Model": config[model_config]["model"],
                            "Config": model_config,
                            "Status": "Success",
                            "Details": "Command executed successfully",
                            "Response Time": response_time,
                            "Token Count": token_count,
                        }
                    )

                    # Save test summary to YAML
                    metrics.save_test_summary(
                        provider,
                        config[model_config]["model"],
                        model_config,
                        prompt,
                        "Success",
                        "Command executed successfully",
                        response_time,
                        token_count,
                    )

                except Exception as e:
                    error_message = str(e)
                    console.print(
                        f"An error occurred: {error_message}", style="bold red"
                    )
                    summary.append(
                        {
                            "Provider": provider,
                            "Model": config[model_config]["model"],
                            "Config": model_config,
                            "Status": "Error",
                            "Details": error_message,
                            "Response Time": float("inf"),
                            "Token Count": "N/A",
                        }
                    )

                    # Save error summary to YAML
                    metrics.save_test_summary(
                        provider,
                        config[model_config]["model"],
                        model_config,
                        prompt,
                        "Error",
                        error_message,
                        float("inf"),
                        "N/A",
                    )

    finally:
        # Revert to the original configuration
        config[model_config]["provider"] = original_provider
        config[model_config]["model"] = original_model
        configure.save_config(config)

    # Sort summary by response time
    summary.sort(key=lambda x: x["Response Time"])

    console.print("\nTest Summary:", style="bold underline")
    table = Table(title="Test Results (Sorted by Response Time)", box=box.ROUNDED)
    table.add_column("Provider", style="cyan")
    table.add_column("Model", style="magenta")
    table.add_column("Config", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Details", style="white")
    table.add_column("Response Time", style="cyan")
    table.add_column("Token Count", style="orange3")

    for entry in summary:
        status_style = "green" if entry["Status"] == "Success" else "red"
        response_time = (
            f"{entry['Response Time']:.2f}s"
            if isinstance(entry["Response Time"], float)
            and entry["Response Time"] != float("inf")
            else "N/A"
        )
        table.add_row(
            entry["Provider"],
            entry["Model"],
            entry["Config"],
            f"[{status_style}]{entry['Status']}[/{status_style}]",
            entry["Details"],
            response_time,
            str(entry["Token Count"]),
        )

    console.print(table)

    success_count = sum(1 for entry in summary if entry["Status"] == "Success")
    total_count = len(summary)
    success_rate = (success_count / total_count) * 100 if total_count > 0 else 0

    console.print(f"\nTotal tests: {total_count}")
    console.print(f"Successful tests: {success_count}")
    console.print(f"Success rate: {success_rate:.2f}%")

    console.print("\nTest completed.", style="bold green")
