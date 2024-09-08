import os
import random
import re
import string
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List

import yaml
from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()


class Auditor:
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data
        self.timestamps = [
            datetime.fromisoformat(entry["timestamp"]) for entry in self.data
        ]
        self.commands = [entry["command"].split()[0] for entry in self.data]
        self.stop_words = set(
            [
                "a",
                "an",
                "and",
                "are",
                "as",
                "at",
                "be",
                "by",
                "for",
                "from",
                "has",
                "he",
                "in",
                "is",
                "it",
                "its",
                "of",
                "on",
                "that",
                "the",
                "to",
                "was",
                "were",
                "will",
                "with",
            ]
        )
        self.excluded_words = set(
            [
                "what",
                "list",
                "none",
                "create",
                "write",
                "generate",
                "describe",
                "explain",
                "given",
                "based",
                "these",
                "table",
                "most",
                "important",
            ]
        )

    def generate_colored_terminal_word_cloud(self, width=80, height=20):
        # Combine all prompts into a single string
        text = " ".join(self._get_all_prompt_text(entry) for entry in self.data)

        # Remove punctuation and split into words
        translator = str.maketrans("", "", string.punctuation)
        words = re.findall(r"\b\w+\b", text.translate(translator).lower())

        # Count word frequencies
        word_counts = Counter(
            word
            for word in words
            if word not in self.stop_words
            and word not in self.excluded_words
            and len(word) > 3
        )

        # Select top words
        top_words = dict(word_counts.most_common(100))

        # Normalize frequencies
        max_freq = max(top_words.values())
        min_freq = min(top_words.values())
        freq_range = max_freq - min_freq

        # Color scale (from cool to warm colors)
        color_scale = ["bright_blue", "cyan", "green", "yellow", "red"]

        # Generate cloud
        cloud = [[" " for _ in range(width)] for _ in range(height)]
        placed_words = []
        for word, freq in top_words.items():
            normalized_freq = (freq - min_freq) / freq_range
            color_index = int(normalized_freq * (len(color_scale) - 1))
            color = color_scale[color_index]

            for _ in range(50):  # Try to place each word up to 50 times
                x = random.randint(0, width - len(word))
                y = random.randint(0, height - 1)
                if all(cloud[y][x + i] == " " for i in range(len(word))):
                    placed_words.append((x, y, word, color))
                    for i in range(len(word)):
                        cloud[y][x + i] = "#"  # Placeholder
                    break

        # Convert cloud to Rich Text object
        console = Console()
        text_cloud = Text()
        for row in cloud:
            for char in row:
                text_cloud.append(char)
            text_cloud.append("\n")

        # Replace placeholders with colored words
        for x, y, word, color in placed_words:
            pos = y * (width + 1) + x  # +1 for newline characters
            text_cloud = (
                text_cloud[:pos]
                + Text(word, style=color)
                + text_cloud[pos + len(word) :]
            )

        return text_cloud

    def command_frequency_analysis(self):
        command_counter = Counter(self.commands)
        return command_counter.most_common()

    def file_operation_analysis(self):
        reads = sum(1 for entry in self.data if entry.get("source_file"))
        writes = sum(1 for entry in self.data if entry.get("destination_file"))
        extensions = Counter(
            self._get_file_extension(entry.get("destination_file", ""))
            for entry in self.data
            if entry.get("destination_file")
        )
        source_folders = Counter(
            self._get_folder(entry.get("source_file", ""))
            for entry in self.data
            if entry.get("source_file")
        )
        destination_folders = Counter(
            self._get_folder(entry.get("destination_file", ""))
            for entry in self.data
            if entry.get("destination_file")
        )
        return {
            "read_write_ratio": reads / writes if writes else float("inf"),
            "common_extensions": extensions.most_common(5),
            "common_source_folders": source_folders.most_common(5),
            "common_destination_folders": destination_folders.most_common(5),
        }

    def _get_all_prompt_text(self, entry):
        prompts = []
        if entry.get("prompt"):
            prompts.append(entry["prompt"])
        if entry.get("custom_prompt"):
            prompts.append(entry["custom_prompt"])
        if entry.get("command"):
            command_parts = entry["command"].split("--prompt=")
            if len(command_parts) > 1:
                prompts.append(command_parts[1].split()[0])
        return " ".join(prompts)

    def prompt_analysis(self):
        all_prompts = [self._get_all_prompt_text(entry) for entry in self.data]
        words = [
            word.lower()
            for prompt in all_prompts
            for word in re.findall(r"\w+", prompt)
            if word.lower() not in self.stop_words
            and len(word) > 4
            and word.lower() not in self.excluded_words
        ]
        keywords = Counter(words)
        bigrams = Counter(
            bigram
            for bigram in self._get_bigrams(words)
            if not any(word in self.excluded_words for word in bigram.split())
        )
        non_empty_prompts = [prompt for prompt in all_prompts if prompt.strip()]
        avg_length = (
            sum(len(prompt.split()) for prompt in non_empty_prompts)
            / len(non_empty_prompts)
            if non_empty_prompts
            else 0
        )
        task_types = Counter(self._categorize_task(prompt) for prompt in all_prompts)
        task_types = Counter(
            {k: v for k, v in task_types.items() if k not in self.excluded_words}
        )
        return {
            "common_keywords": keywords.most_common(10),
            "common_bigrams": bigrams.most_common(5),
            "average_prompt_length": avg_length,
            "task_types": task_types.most_common(),
        }

    def time_based_analysis(self):
        hours = Counter(timestamp.hour for timestamp in self.timestamps)
        weekdays = Counter(timestamp.strftime("%A") for timestamp in self.timestamps)
        intervals = [
            int((t2 - t1).total_seconds())
            for t1, t2 in zip(self.timestamps, self.timestamps[1:])
        ]
        avg_interval = sum(intervals) / len(intervals) if intervals else 0
        return {
            "peak_hours": hours.most_common(3),
            "busiest_days": weekdays.most_common(3),
            "average_time_between_commands": avg_interval / 60,  # in minutes
        }

    def user_behavior_analysis(self):
        command_pairs = Counter(
            tuple(pair) for pair in zip(self.commands, self.commands[1:])
        )
        prompt_complexity = [
            (entry["timestamp"], len(self._get_all_prompt_text(entry).split()))
            for entry in self.data
        ]
        formatted_complexity = [
            (
                datetime.fromisoformat(timestamp).strftime("%m/%d (%I:%M%p)").lower(),
                complexity,
            )
            for timestamp, complexity in prompt_complexity[-5:]
        ]
        return {
            "common_command_sequences": command_pairs.most_common(5),
            "prompt_complexity_over_time": formatted_complexity,
        }

    def command_prompt_distribution(self):
        distributions = {
            "with_user_prompt": 0,
            "with_custom_prompt": 0,
            "with_prompt_file": 0,
            "without_prompt": 0,
        }
        for entry in self.data:
            if entry.get("prompt"):
                distributions["with_user_prompt"] += 1
            elif entry.get("custom_prompt"):
                distributions["with_custom_prompt"] += 1
            elif entry.get("prompt_file"):
                distributions["with_prompt_file"] += 1
            else:
                distributions["without_prompt"] += 1
        return distributions

    def create_ascii_timeline(self, width=40, height=10):
        if not self.timestamps or not self.commands:
            return "No data to display"

        start_time = min(self.timestamps)
        end_time = max(self.timestamps)
        time_range = (end_time - start_time).total_seconds()

        grid = [[" " for _ in range(width + 3)] for _ in range(height + 2)]
        column_counts = [0] * width

        for timestamp in self.timestamps:
            relative_time = (timestamp - start_time).total_seconds()
            x = int((relative_time / time_range) * (width - 1))
            column_counts[x] += 1

        max_count = max(column_counts) if column_counts else 1

        for x, count in enumerate(column_counts):
            bar_height = int((count / max_count) * (height - 1))
            for y in range(height - 1, height - 1 - bar_height, -1):
                grid[y][x + 3] = "█"

        for i in range(height):
            grid[i][2] = "│"

        for i in range(3, width + 3):
            grid[height][i] = "─"

        grid[height][2] = "└"

        mid_time = start_time + (end_time - start_time) / 2
        start_label = start_time.strftime("%m-%d")
        mid_label = mid_time.strftime("%m-%d")
        end_label = end_time.strftime("%m-%d")

        label_row = [" ", " ", " "] + [" "] * width
        label_row[3 : 3 + len(start_label)] = start_label
        label_row[width // 2 : width // 2 + len(mid_label)] = mid_label
        label_row[-len(end_label) :] = end_label
        grid[height + 1] = label_row

        grid[0][0:2] = list(f"{max_count:2d}")
        grid[height // 2][0:2] = list(f"{max_count // 2:2d}")
        grid[height - 1][0:2] = list(" 0")

        timeline_str = "\n".join("".join(row) for row in grid)
        return timeline_str

    def generate_markdown_report(self):
        report = "# Trail Analysis Report\n\n"

        report += "## General Analysis\n"
        report += "| Metric | Value |\n|--------|-------|\n"

        command_freq = self.command_frequency_analysis()[:3]
        file_ops = self.file_operation_analysis()
        time_analysis = self.time_based_analysis()

        report += f"| Top 3 Commands | {', '.join(f'{cmd[0]} ({cmd[1]} times)' for cmd in command_freq)} |\n"
        report += f"| Read/Write Ratio | {file_ops['read_write_ratio']:.2f} |\n"
        report += f"| Top 3 Extensions | {', '.join(f'{ext[0]} ({ext[1]} times)' for ext in file_ops['common_extensions'][:3])} |\n"
        report += f"| Top 3 Source Folders | {', '.join(f'{folder[0]} ({folder[1]} times)' for folder in file_ops['common_source_folders'][:3])} |\n"
        report += f"| Top 3 Destination Folders | {', '.join(f'{folder[0]} ({folder[1]} times)' for folder in file_ops['common_destination_folders'][:3])} |\n"
        report += f"| Top 3 Peak Hours | {', '.join(f'{hour[0]}:00 ({hour[1]} commands)' for hour in time_analysis['peak_hours'])} |\n"
        report += f"| Top 3 Busiest Days | {', '.join(f'{day[0]} ({day[1]} commands)' for day in time_analysis['busiest_days'])} |\n"
        report += f"| Avg Time Between Commands | {time_analysis['average_time_between_commands']} seconds |\n"

        report += "\n## Prompt Word Cloud\n"
        report += "```\n"
        report += self.generate_colored_terminal_word_cloud().plain
        report += "\n```\n"
        report += "\nNote: Colors in the word cloud represent frequency (blue: least frequent, red: most frequent)\n"

        prompt_analysis = self.prompt_analysis()
        report += "\n## Prompt Analysis\n"
        report += "| Metric | Value |\n|--------|-------|\n"
        report += f"| Average Prompt Length | {prompt_analysis['average_prompt_length']:.2f} words |\n"
        report += (
            "| Top Keywords | "
            + ", ".join(
                f"{word} ({count})"
                for word, count in prompt_analysis["common_keywords"][:5]
            )
            + " |\n"
        )
        report += (
            "| Top Bigrams | "
            + ", ".join(
                f"{bigram.replace('_', ' ')} ({count})"
                for bigram, count in prompt_analysis["common_bigrams"]
            )
            + " |\n"
        )
        report += (
            "| Task Types | "
            + ", ".join(
                f"{task} ({count})" for task, count in prompt_analysis["task_types"]
            )
            + " |\n"
        )

        behavior_analysis = self.user_behavior_analysis()
        report += "\n## User Behavior Analysis\n"
        report += "| Metric | Value |\n|--------|-------|\n"
        report += (
            "| Common Command Sequences | "
            + ", ".join(
                f"{cmd1} → {cmd2} ({count})"
                for (cmd1, cmd2), count in behavior_analysis["common_command_sequences"]
            )
            + " |\n"
        )
        report += (
            "| Recent Prompt Complexity | "
            + ", ".join(
                f"{timestamp}: {complexity} words"
                for timestamp, complexity in behavior_analysis[
                    "prompt_complexity_over_time"
                ]
            )
            + " |\n"
        )

        command_dist = self.command_prompt_distribution()
        report += "\n## Command Distribution\n"
        report += "| Prompt Type | Count |\n|-------------|-------|\n"
        for prompt_type, count in command_dist.items():
            report += f"| {prompt_type.replace('_', ' ').title()} | {count} |\n"

        report += "\n## Command Frequency Timeline\n"
        report += "```\n" + self.create_ascii_timeline() + "\n```\n"

        return report

    @staticmethod
    def _get_file_extension(filename):
        return filename.split(".")[-1] if "." in filename else "no_extension"

    @staticmethod
    def _get_folder(filename):
        return filename.split("/")[0] if "/" in filename else "root"

    @staticmethod
    def _categorize_task(prompt):
        if "table" in prompt.lower():
            return "create table"
        elif "function" in prompt.lower():
            return "write function"
        elif any(word in prompt.lower() for word in ["explain", "what is", "how"]):
            return "explanation"
        else:
            return "other"

    @staticmethod
    def _get_bigrams(words):
        return [" ".join(pair) for pair in zip(words, words[1:])]


def trail_auditor(filename: str):
    with open(filename, "r") as f:
        data = yaml.safe_load(f)

    auditor = Auditor(data)

    console.print("[bold]Trail Analysis Report:[/bold]")

    general_table = Table(title="General Analysis")
    general_table.add_column("Metric", style="cyan")
    general_table.add_column("Value", style="green")

    command_freq = auditor.command_frequency_analysis()[:3]
    file_ops = auditor.file_operation_analysis()
    time_analysis = auditor.time_based_analysis()

    general_table.add_row(
        "Top 3 Commands",
        ", ".join(f"{cmd[0]} ({cmd[1]} times)" for cmd in command_freq),
    )
    general_table.add_row("Read/Write Ratio", f"{file_ops['read_write_ratio']:.2f}")
    general_table.add_row(
        "Top 3 Extensions",
        ", ".join(
            f"{ext[0]} ({ext[1]} times)" for ext in file_ops["common_extensions"][:3]
        ),
    )
    general_table.add_row(
        "Top 3 Source Folders",
        ", ".join(
            f"{folder[0]} ({folder[1]} times)"
            for folder in file_ops["common_source_folders"][:3]
        ),
    )
    general_table.add_row(
        "Top 3 Destination Folders",
        ", ".join(
            f"{folder[0]} ({folder[1]} times)"
            for folder in file_ops["common_destination_folders"][:3]
        ),
    )
    general_table.add_row(
        "Top 3 Peak Hours",
        ", ".join(
            f"{hour[0]}:00 ({hour[1]} commands)" for hour in time_analysis["peak_hours"]
        ),
    )
    general_table.add_row(
        "Top 3 Busiest Days",
        ", ".join(
            f"{day[0]} ({day[1]} commands)" for day in time_analysis["busiest_days"]
        ),
    )
    general_table.add_row(
        "Avg Time Between Commands",
        f"{round(time_analysis['average_time_between_commands'], 2)} minutes",
    )

    console.print(general_table)

    console.print("\n[bold]Prompt Word Cloud:[/bold]")
    console.print(auditor.generate_colored_terminal_word_cloud())
    console.print(
        "Colors represent frequency (blue: least frequent, red: most frequent)"
    )

    prompt_analysis = auditor.prompt_analysis()
    prompt_table = Table(title="Prompt Analysis")
    prompt_table.add_column("Metric", style="cyan")
    prompt_table.add_column("Value", style="green")

    prompt_table.add_row(
        "Average Prompt Length", f"{prompt_analysis['average_prompt_length']:.2f} words"
    )
    prompt_table.add_row(
        "Top Keywords",
        ", ".join(
            f"{word} ({count})"
            for word, count in prompt_analysis["common_keywords"][:5]
        ),
    )
    prompt_table.add_row(
        "Top Bigrams",
        ", ".join(
            f"{bigram} ({count})" for bigram, count in prompt_analysis["common_bigrams"]
        ),
    )
    prompt_table.add_row(
        "Task Types",
        ", ".join(f"{task} ({count})" for task, count in prompt_analysis["task_types"]),
    )

    console.print(prompt_table)

    behavior_analysis = auditor.user_behavior_analysis()
    behavior_table = Table(title="User Behavior Analysis")
    behavior_table.add_column("Metric", style="cyan")
    behavior_table.add_column("Value", style="green")

    behavior_table.add_row(
        "Common Command Sequences",
        ", ".join(
            f"{cmd1} → {cmd2} ({count})"
            for (cmd1, cmd2), count in behavior_analysis["common_command_sequences"]
        ),
    )
    behavior_table.add_row(
        "Recent Prompt Complexity",
        ", ".join(
            f"{timestamp}: {complexity} words"
            for timestamp, complexity in behavior_analysis[
                "prompt_complexity_over_time"
            ]
        ),
    )

    console.print(behavior_table)

    command_dist = auditor.command_prompt_distribution()
    dist_table = Table(title="Command Distribution")
    dist_table.add_column("Prompt Type", style="cyan")
    dist_table.add_column("Count", style="green")

    for prompt_type, count in command_dist.items():
        dist_table.add_row(prompt_type.replace("_", " ").title(), str(count))

    console.print(dist_table)

    console.print("\n[bold]Command Frequency Timeline:[/bold]")
    console.print(auditor.create_ascii_timeline())

    # Generate and save markdown report
    report = auditor.generate_markdown_report()
    os.makedirs("Audits", exist_ok=True)
    report_filename = (
        f"Audits/trail_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    )
    with open(report_filename, "w") as f:
        f.write(report)

    console.print(
        f"\n[bold green]Markdown report saved as {report_filename}[/bold green]"
    )
