import os
import re
from difflib import SequenceMatcher
from math import ceil
from pathlib import Path

import tiktoken
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from navamai import configure

console = Console()


def split_text_by_tokens(file_path, model="gpt-3.5-turbo"):
    config = configure.load_config()
    split_config = config.get("split")
    target_model = split_config.get("model")
    ratio = split_config.get("context-ratio")
    context_config = config.get("model-context")
    context_window = context_config.get(target_model)
    token_limit = round(context_window * ratio, 0)
    # Initialize the tokenizer
    enc = tiktoken.encoding_for_model(model)

    # Read the entire file
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Tokenize the entire text
    tokens = enc.encode(text)

    # Split the tokens into chunks
    chunks = []
    current_chunk = []
    current_chunk_tokens = 0

    for token in tokens:
        if current_chunk_tokens + 1 > token_limit:
            chunks.append(enc.decode(current_chunk))
            current_chunk = []
            current_chunk_tokens = 0

        current_chunk.append(token)
        current_chunk_tokens += 1

    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(enc.decode(current_chunk))

    # Write chunks to separate files
    base_name = os.path.splitext(file_path)[0]
    for i, chunk in enumerate(chunks):
        output_file = f"{base_name} - part {i+1}.txt"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(chunk)

    return len(chunks)


def extract_variables(template):
    # Regular expression pattern to match variables enclosed in double curly braces
    pattern = r"\{\{(\w+)\}\}"

    # Find all matches in the template
    matches = re.findall(pattern, template)

    # Return the list of unique variable names
    return list(set(matches))


def list_files(directory, page=1, files_per_page=10, extensions=None):
    all_files = [
        f
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
        and (extensions is None or any(f.endswith(ext) for ext in extensions))
    ]
    all_files.sort()  # Sort the files alphabetically
    total_pages = ceil(len(all_files) / files_per_page)
    start = (page - 1) * files_per_page
    end = start + files_per_page
    return all_files[start:end], total_pages

def count_tokens(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(content))


def intent_select_paginate(sections, page=1, intents_per_page=10):
    total_pages = ceil(len(sections) / intents_per_page)

    while True:
        start = (page - 1) * intents_per_page
        end = start + intents_per_page
        current_sections = sections[start:end]

        table = Table(title=f"Available Intents (Page {page} of {total_pages})")
        table.add_column("Number", no_wrap=True)
        table.add_column("Intent Title", style="cyan")

        for i, (title, _) in enumerate(current_sections, start + 1):
            table.add_row(str(i), title)

        console.print(table)

        if total_pages > 1:
            msg = "Enter intent number, '[blue]n[/blue]' for next page, '[blue]p[/blue]' for previous page, or '[blue]q[/blue]' to quit"
        else:
            msg = "Enter intent number or '[blue]q[/blue]' to quit"

        choice = Prompt.ask(msg, default="")

        if choice.lower() == "q":
            return None
        elif choice.lower() == "n" and page < total_pages:
            page += 1
        elif choice.lower() == "p" and page > 1:
            page -= 1
        elif choice.isdigit() and 1 <= int(choice) <= len(sections):
            selected_index = int(choice) - 1
            return sections[selected_index]
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")


def file_select_paginate(directory, show_tokens=False, section=None, extensions=None):
    page = 1
    files_per_page = 10
    while True:
        files, total_pages = list_files(
            directory, page, files_per_page, extensions=extensions
        )

        extensions_str = ", ".join(extensions) if extensions else "All"
        table = Table(title=f"{extensions_str} Files (Page {page} of {total_pages})")
        table.add_column("Number", no_wrap=True)
        table.add_column("Filename", style="cyan")
        if show_tokens:
            table.add_column("Tokens", style="green")
            table.add_column("Context", style="magenta")

        for i, file in enumerate(files, 1):
            file_path = os.path.join(directory, file)
            if show_tokens:
                config = configure.load_config()
                model_config = config.get(section)
                model_context = config.get("model-context")
                context_length = model_context.get(model_config.get("model"))
                tokens = count_tokens(file_path)
                context_ratio = round(tokens / context_length * 100, 2)
                token_display = f"{tokens / 1000:.1f}K"
                context_display = f"{context_ratio}%"
                table.add_row(str(i), file, token_display, context_display)
            else:
                table.add_row(str(i), file)

        console.print(table)
        if total_pages > 1:
            msg = "Enter file number, '[blue]n[/blue]' for next page, '[blue]p[/blue]' for previous page, or '[blue]q[/blue]' to quit"
        else:
            msg = "Enter file number or '[blue]q[/blue]' to quit"

        choice = Prompt.ask(msg, default="")

        if choice.lower() == "q":
            return None
        elif choice.lower() == "n" and page < total_pages:
            page += 1
        elif choice.lower() == "p" and page > 1:
            page -= 1
        elif choice.isdigit() and 1 <= int(choice) <= len(files):
            return os.path.join(directory, files[int(choice) - 1])
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")

def merge_docs(
    source_path,
    dest_suffix="expanded",
    merge_suffix="merged",
    placeholder="[merge here]",
    prompt_prefix="> Prompt:",
):

    # Step 1: Read source content
    source_file = source_path + ".md"
    with open(source_file, "r") as f:
        source_content = f.read()

    # Step 2: Read expanded content
    expanded_file = source_path + f" {dest_suffix}.md"
    with open(expanded_file, "r") as f:
        expanded_content = f.read()

    # Step 3: Define merged doc path
    merged_file = source_path + f" {merge_suffix}.md"

    # Step 4: Remove sentences starting with prompt prefix from source_content

    escaped_prefix = re.escape(prompt_prefix)
    source_content = re.sub(rf"(?m)^{escaped_prefix}.*$\n?", "", source_content)

    # Step 5 & 6: Find placeholders, match headings, and replace content
    # Split expanded content into lines
    expanded_lines = expanded_content.split("\n")

    # Initialize variables
    current_heading = ""
    merged_lines = []
    section_buffer = []

    def process_section():
        nonlocal section_buffer, merged_lines
        if not section_buffer:
            return

        merge_index = next(
            (i for i, line in enumerate(section_buffer) if f"{placeholder}" in line), -1
        )

        if merge_index != -1:
            # Add content before [merge here]
            merged_lines.extend(section_buffer[:merge_index])

            # Find and add corresponding content from source
            match = re.search(
                f"{re.escape(current_heading)}(.*?)(?=\n#|$)", source_content, re.DOTALL
            )
            if match:
                merged_content = match.group(1).strip().split("\n")
                # Remove the heading if it's the first line of merged_content
                if merged_content and merged_content[0].startswith("#"):
                    merged_content = merged_content[1:]
                merged_lines.extend(merged_content)

            # Add content after [merge here]
            merged_lines.extend(section_buffer[merge_index + 1 :])
        else:
            # If no [merge here], add entire section
            merged_lines.extend(section_buffer)

        section_buffer.clear()

    for line in expanded_lines:
        if line.startswith("#"):
            process_section()
            current_heading = line
            section_buffer = [line]
        else:
            section_buffer.append(line)

    # Process the last section
    process_section()

    # Step 7: Save as merged doc
    with open(merged_file, "w") as f:
        f.write("\n".join(merged_lines))

    print(f"Merged document saved as: {merged_file}")


def diff(content1, content2):
    def preprocess_content(content):
        # Remove newlines and extra whitespace
        content = re.sub(r"\s+", " ", content)
        # Remove all markdown formatting
        content = re.sub(r"[#*_`~\[\]()>]+", "", content)
        # Remove links
        content = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", content)
        # Remove HTML tags
        content = re.sub(r"<[^>]+>", "", content)
        return content.strip().lower()

    # Preprocess both contents
    processed_content1 = preprocess_content(content1)
    processed_content2 = preprocess_content(content2)

    # Calculate similarity ratio
    similarity = SequenceMatcher(None, processed_content1, processed_content2).ratio()

    # Calculate difference percentage
    difference_percentage = (1 - similarity) * 100

    return difference_percentage


def parse_markdown_sections(content):
    pattern = r"^#\s(.+)\n\nPrompt:\s(.+)$"
    return re.findall(pattern, content, re.MULTILINE)


def update_markdown_with_response(filename, title, response_filename):
    with open(filename, "r") as file:
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
        updated_content = (
            content[: match.start()] + replacement + "\n\n" + content[match.end() :]
        )
    else:
        # Section not found, don't modify the file
        return

    with open(filename, "w") as file:
        file.write(updated_content)
