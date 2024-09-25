# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import os
from datetime import datetime, timedelta

import tiktoken
import yaml
from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def count_tokens(text):
    """Count the number of tokens in the given text."""
    try:
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        return len(encoding.encode(text))
    except Exception:
        # Fallback to a simple word count if tiktoken fails
        return len(text.split())


def generate_yaml_data(
    provider, model, config, prompt, status, details, response_time, token_count
):
    timestamp = datetime.now().isoformat()
    return {
        timestamp: {
            provider: {
                model: {
                    config: {
                        "prompt": prompt,
                        "status": status,
                        "details": details,
                        "response_time": response_time,
                        "token_count": token_count,
                    }
                }
            }
        }
    }


def save_to_yaml(data):
    filename = f"Metrics/test_summary_{datetime.now().strftime('%Y%m%d')}.yml"

    if os.path.exists(filename):
        with open(filename, "r") as file:
            existing_data = yaml.safe_load(file) or {}
    else:
        existing_data = {}

    existing_data.update(data)

    with open(filename, "w") as file:
        yaml.dump(existing_data, file, default_flow_style=False)


def save_test_summary(
    provider, model, model_config, prompt, status, details, response_time, token_count
):
    yaml_data = generate_yaml_data(
        provider,
        model,
        model_config,
        prompt,
        status,
        details,
        response_time,
        token_count,
    )
    save_to_yaml(yaml_data)


def read_yaml_files(directory="Metrics"):
    data = {}
    for filename in os.listdir(directory):
        if filename.startswith("test_summary_") and filename.endswith(".yml"):
            date = filename[13:21]  # Extract date from filename
            with open(os.path.join(directory, filename), "r") as file:
                data[date] = yaml.safe_load(file)
    console.print(f"Found {len(data)} YAML files")
    return data


def process_data(data, days=7):
    processed_data = {}
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days - 1)

    for date, daily_data in data.items():
        file_date = datetime.strptime(date, "%Y%m%d").date()
        if start_date <= file_date <= end_date:
            for timestamp, provider_data in daily_data.items():
                for provider, model_data in provider_data.items():
                    for model, config_data in model_data.items():
                        for config, test_data in config_data.items():
                            key = (provider, model, config)
                            if key not in processed_data:
                                processed_data[key] = {
                                    "dates": [],
                                    "response_times": [],
                                    "token_counts": [],
                                }
                            processed_data[key]["dates"].append(file_date)
                            processed_data[key]["response_times"].append(
                                test_data["response_time"]
                            )
                            processed_data[key]["token_counts"].append(
                                test_data["token_count"]
                            )

    console.print(
        f"Processed data for {len(processed_data)} provider-model combinations"
    )
    return processed_data


def create_sparkline(data, max_value, width=10):
    if not data:
        return " " * width

    bins = [0] * width
    for value in data:
        if isinstance(value, (int, float)) and value != float("inf"):
            bin = min(int((value / max_value) * (width - 1)), width - 1)
            bins[bin] += 1

    sparkline = ""
    for count in bins:
        if count == 0:
            sparkline += "▁"
        elif count <= 1:
            sparkline += "▂"
        elif count <= 2:
            sparkline += "▃"
        elif count <= 3:
            sparkline += "▄"
        elif count <= 4:
            sparkline += "▅"
        else:
            sparkline += "▇"

    return sparkline


def display_trends(processed_data):
    if not processed_data:
        console.print("No data to display", style="bold red")
        return

    console.print(Panel("Trend Visualization", style="bold magenta"))

    tables = []
    for (provider, model, config), data in processed_data.items():
        table = Table(
            title=f"{provider} - {model} ({config})", box=box.ROUNDED, width=60
        )
        table.add_column("Metric", style="cyan", width=15)
        table.add_column("Trend", style="magenta", width=12)
        table.add_column("Min", style="green", width=8)
        table.add_column("Max", style="red", width=8)
        table.add_column("Avg", style="yellow", width=8)

        # Response Time
        rt_data = [
            rt
            for rt in data["response_times"]
            if isinstance(rt, (int, float)) and rt != float("inf")
        ]
        if rt_data:
            rt_max = max(rt_data)
            rt_sparkline = create_sparkline(rt_data, rt_max)
            table.add_row(
                "Response Time",
                rt_sparkline,
                f"{min(rt_data):.2f}s",
                f"{rt_max:.2f}s",
                f"{sum(rt_data)/len(rt_data):.2f}s",
            )

        # Token Count
        tc_data = [
            tc
            for tc in data["token_counts"]
            if isinstance(tc, (int, float)) and tc != "N/A"
        ]
        if tc_data:
            tc_max = max(tc_data)
            tc_sparkline = create_sparkline(tc_data, tc_max)
            table.add_row(
                "Token Count",
                tc_sparkline,
                str(min(tc_data)),
                str(max(tc_data)),
                f"{sum(tc_data)/len(tc_data):.2f}",
            )

        tables.append(table)

    # Display tables with pagination
    items_per_page = 4
    for i in range(0, len(tables), items_per_page):
        page_tables = tables[i : i + items_per_page]
        console.print(Columns(page_tables))
        if i + items_per_page < len(tables):
            input("Press Enter to see more...")
            console.clear()
