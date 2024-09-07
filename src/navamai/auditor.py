import yaml
from collections import Counter
from datetime import datetime, timedelta
import re
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
import os

console = Console()

class Auditor:
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data
        self.timestamps = [datetime.fromisoformat(entry['timestamp']) for entry in self.data]
        self.commands = [entry['command'].split()[0] for entry in self.data]
        self.stop_words = set(['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it',
                               'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were', 'will', 'with'])

    def command_frequency_analysis(self):
        command_counter = Counter(self.commands)
        return command_counter.most_common()

    def file_operation_analysis(self):
        reads = sum(1 for entry in self.data if entry.get('source_file'))
        writes = sum(1 for entry in self.data if entry.get('destination_file'))
        extensions = Counter(self._get_file_extension(entry.get('destination_file', '')) for entry in self.data if entry.get('destination_file'))
        folders = Counter(self._get_folder(entry.get('destination_file', '')) for entry in self.data if entry.get('destination_file'))
        return {
            'read_write_ratio': reads / writes if writes else float('inf'),
            'common_extensions': extensions.most_common(5),
            'common_folders': folders.most_common(5)
        }

    def prompt_analysis(self):
        prompts = [entry.get('prompt', '') for entry in self.data if entry.get('prompt')]
        words = [word.lower() for prompt in prompts for word in re.findall(r'\w+', prompt) if word.lower() not in self.stop_words]
        keywords = Counter(words)
        bigrams = Counter(self._get_bigrams(words))
        avg_length = sum(len(prompt.split()) for prompt in prompts) / len(prompts) if prompts else 0
        task_types = Counter(self._categorize_task(prompt) for prompt in prompts)
        return {
            'common_keywords': keywords.most_common(10),
            'common_bigrams': bigrams.most_common(5),
            'average_prompt_length': avg_length,
            'task_types': task_types.most_common()
        }

    def time_based_analysis(self):
        hours = Counter(timestamp.hour for timestamp in self.timestamps)
        weekdays = Counter(timestamp.strftime('%A') for timestamp in self.timestamps)
        intervals = [int((t2 - t1).total_seconds()) for t1, t2 in zip(self.timestamps, self.timestamps[1:])]
        avg_interval = sum(intervals) / len(intervals) if intervals else 0
        return {
            'peak_hours': hours.most_common(3),
            'busiest_days': weekdays.most_common(),
            'average_time_between_commands': timedelta(seconds=avg_interval)
        }

    def user_behavior_analysis(self):
        command_pairs = Counter(tuple(pair) for pair in zip(self.commands, self.commands[1:]))
        prompt_complexity = [(entry['timestamp'], len(entry.get('prompt', '').split())) 
                             for entry in self.data if entry.get('prompt')]
        return {
            'common_command_sequences': command_pairs.most_common(5),
            'prompt_complexity_over_time': prompt_complexity
        }

    def create_ascii_timeline(self, width=80, height=20):
        if not self.timestamps or not self.commands:
            return "No data to display"

        start_time = min(self.timestamps)
        end_time = max(self.timestamps)
        time_range = (end_time - start_time).total_seconds()

        # Create grid with extra space for axes
        grid = [[' ' for _ in range(width + 3)] for _ in range(height + 2)]  # +2 for x-axis and labels

        # Count events for each column
        column_counts = [0] * width

        for timestamp in self.timestamps:
            relative_time = (timestamp - start_time).total_seconds()
            x = int((relative_time / time_range) * (width - 1))
            column_counts[x] += 1

        # Find the maximum count for scaling
        max_count = max(column_counts) if column_counts else 1

        # Add bars
        for x, count in enumerate(column_counts):
            bar_height = int((count / max_count) * (height - 1))
            for y in range(height - 1, height - 1 - bar_height, -1):
                grid[y][x + 3] = '█'  # Using full block character for bars

        # Add y-axis
        for i in range(height):
            grid[i][2] = '│'
        
        # Add x-axis
        for i in range(3, width + 3):
            grid[height][i] = '─'
        
        # Add origin
        grid[height][2] = '└'

        # Add time labels on x-axis
        mid_time = start_time + (end_time - start_time) / 2
        start_label = start_time.strftime('%m-%d')
        mid_label = mid_time.strftime('%m-%d')
        end_label = end_time.strftime('%m-%d')
        
        # Place labels at start, middle, and end of x-axis
        label_row = [' ', ' ', ' '] + [' '] * width
        label_row[3:3+len(start_label)] = start_label
        label_row[width//2:width//2+len(mid_label)] = mid_label
        label_row[-len(end_label):] = end_label
        grid[height + 1] = label_row

        # Add event count indicator on y-axis
        grid[0][0:2] = list(f'{max_count:2d}')
        grid[height // 2][0:2] = list(f'{max_count // 2:2d}')
        grid[height - 1][0:2] = list(' 0')

        timeline_str = '\n'.join(''.join(row) for row in grid)
        return timeline_str

    def generate_markdown_report(self):
        report = "# Trail Analysis Report\n\n"

        report += "## General Analysis\n"
        report += "| Metric | Value |\n|--------|-------|\n"
        
        command_freq = self.command_frequency_analysis()[:5]
        file_ops = self.file_operation_analysis()
        time_analysis = self.time_based_analysis()
        
        report += f"| Top Command | {command_freq[0][0]} ({command_freq[0][1]} times) |\n"
        report += f"| Read/Write Ratio | {file_ops['read_write_ratio']:.2f} |\n"
        report += f"| Most Common Extension | {file_ops['common_extensions'][0][0]} ({file_ops['common_extensions'][0][1]} times) |\n"
        report += f"| Most Common Folder | {file_ops['common_folders'][0][0]} ({file_ops['common_folders'][0][1]} times) |\n"
        report += f"| Peak Hour | {time_analysis['peak_hours'][0][0]}:00 ({time_analysis['peak_hours'][0][1]} commands) |\n"
        report += f"| Busiest Day | {time_analysis['busiest_days'][0][0]} ({time_analysis['busiest_days'][0][1]} commands) |\n"
        report += f"| Avg Time Between Commands | {time_analysis['average_time_between_commands']} |\n"

        prompt_analysis = self.prompt_analysis()
        report += "\n## Prompt Analysis\n"
        report += "| Metric | Value |\n|--------|-------|\n"
        report += f"| Average Prompt Length | {prompt_analysis['average_prompt_length']:.2f} words |\n"
        report += "| Top Keywords | " + ", ".join(f"{word} ({count})" for word, count in prompt_analysis['common_keywords'][:5]) + " |\n"
        report += "| Top Bigrams | " + ", ".join(f"{bigram.replace('_', ' ')} ({count})" for bigram, count in prompt_analysis['common_bigrams']) + " |\n"
        report += "| Task Types | " + ", ".join(f"{task} ({count})" for task, count in prompt_analysis['task_types']) + " |\n"

        behavior_analysis = self.user_behavior_analysis()
        report += "\n## User Behavior Analysis\n"
        report += "| Metric | Value |\n|--------|-------|\n"
        report += "| Common Command Sequences | " + ", ".join(f"{cmd1} → {cmd2} ({count})" for (cmd1, cmd2), count in behavior_analysis['common_command_sequences']) + " |\n"
        report += "| Recent Prompt Complexity | " + ", ".join(f"{timestamp}: {complexity} words" for timestamp, complexity in behavior_analysis['prompt_complexity_over_time'][-5:]) + " |\n"

        report += "\n## ASCII Timeline Visualization\n"
        report += "```\n" + self.create_ascii_timeline() + "\n```\n"

        return report

    @staticmethod
    def _get_file_extension(filename):
        return filename.split('.')[-1] if '.' in filename else 'no_extension'

    @staticmethod
    def _get_folder(filename):
        return filename.split('/')[0] if '/' in filename else 'root'

    @staticmethod
    def _categorize_task(prompt):
        if 'table' in prompt.lower():
            return 'create table'
        elif 'function' in prompt.lower():
            return 'write function'
        elif any(word in prompt.lower() for word in ['explain', 'what is', 'how']):
            return 'explanation'
        else:
            return 'other'

    @staticmethod
    def _get_bigrams(words):
        return [' '.join(pair) for pair in zip(words, words[1:])]

def trail_auditor(filename: str):
    with open(filename, 'r') as f:
        data = yaml.safe_load(f)
    
    auditor = Auditor(data)
    
    console.print("[bold]Trail Analysis Report:[/bold]")
        
    general_table = Table(title="General Analysis")
    general_table.add_column("Metric", style="cyan")
    general_table.add_column("Value", style="green")
    
    command_freq = auditor.command_frequency_analysis()[0]
    file_ops = auditor.file_operation_analysis()
    time_analysis = auditor.time_based_analysis()
    
    general_table.add_row("Top Command", f"{command_freq[0]} ({command_freq[1]} times)")
    general_table.add_row("Read/Write Ratio", f"{file_ops['read_write_ratio']:.2f}")
    general_table.add_row("Most Common Extension", f"{file_ops['common_extensions'][0][0]} ({file_ops['common_extensions'][0][1]} times)")
    general_table.add_row("Most Common Folder", f"{file_ops['common_folders'][0][0]} ({file_ops['common_folders'][0][1]} times)")
    general_table.add_row("Peak Hour", f"{time_analysis['peak_hours'][0][0]}:00 ({time_analysis['peak_hours'][0][1]} commands)")
    general_table.add_row("Busiest Day", f"{time_analysis['busiest_days'][0][0]} ({time_analysis['busiest_days'][0][1]} commands)")
    general_table.add_row("Avg Time Between Commands", str(time_analysis['average_time_between_commands']))
    
    console.print(general_table)
    
    prompt_analysis = auditor.prompt_analysis()
    prompt_table = Table(title="Prompt Analysis")
    prompt_table.add_column("Metric", style="cyan")
    prompt_table.add_column("Value", style="green")
    
    prompt_table.add_row("Average Prompt Length", f"{prompt_analysis['average_prompt_length']:.2f} words")
    prompt_table.add_row("Top Keywords", ", ".join(f"{word} ({count})" for word, count in prompt_analysis['common_keywords'][:5]))
    prompt_table.add_row("Top Bigrams", ", ".join(f"{bigram} ({count})" for bigram, count in prompt_analysis['common_bigrams']))
    prompt_table.add_row("Task Types", ", ".join(f"{task} ({count})" for task, count in prompt_analysis['task_types']))
    
    console.print(prompt_table)
    
    behavior_analysis = auditor.user_behavior_analysis()
    behavior_table = Table(title="User Behavior Analysis")
    behavior_table.add_column("Metric", style="cyan")
    behavior_table.add_column("Value", style="green")
    
    behavior_table.add_row("Common Command Sequences", ", ".join(f"{cmd1} → {cmd2} ({count})" for (cmd1, cmd2), count in behavior_analysis['common_command_sequences']))
    behavior_table.add_row("Recent Prompt Complexity", ", ".join(f"{timestamp}: {complexity} words" for timestamp, complexity in behavior_analysis['prompt_complexity_over_time'][-5:]))
    
    console.print(behavior_table)

    console.print("\n[bold]ASCII Timeline Visualization:[/bold]")
    console.print(auditor.create_ascii_timeline())

    # Generate and save markdown report
    report = auditor.generate_markdown_report()
    os.makedirs("Audits", exist_ok=True)
    report_filename = f"Audits/trail_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_filename, "w") as f:
        f.write(report)
    
    console.print(f"\n[bold green]Markdown report saved as {report_filename}[/bold green]")