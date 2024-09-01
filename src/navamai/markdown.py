import re
from difflib import SequenceMatcher


def diff(content1, content2):
    def preprocess_content(content):
        # Remove newlines and extra whitespace
        content = re.sub(r'\s+', ' ', content)
        # Remove all markdown formatting
        content = re.sub(r'[#*_`~\[\]()>]+', '', content)
        # Remove links
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
        # Remove HTML tags
        content = re.sub(r'<[^>]+>', '', content)
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
    pattern = r'^#\s(.+)\n\nPrompt:\s(.+)$'
    return re.findall(pattern, content, re.MULTILINE)

def update_markdown_with_response(filename, title, response_filename):
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