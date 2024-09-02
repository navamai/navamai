import re
from difflib import SequenceMatcher
from pathlib import Path

def merge_docs(file_path):

    # Step 1: Read source content
    source_file = file_path + ".md"
    with open(source_file, 'r') as f:
        source_content = f.read()

    # Step 2: Read expanded content
    expanded_file = file_path + " expanded.md"
    with open(expanded_file, 'r') as f:
        expanded_content = f.read()

    # Step 3: Define merged doc path
    merged_file = file_path + " merged.md"

    # Step 4: Remove sentences starting with "> Prompt:" from source_content
    source_content = re.sub(r'(?m)^> Prompt:.*$\n?', '', source_content)

    # Step 5 & 6: Find placeholders, match headings, and replace content
    # Split expanded content into lines
    expanded_lines = expanded_content.split('\n')
    
    # Initialize variables
    current_heading = ""
    merged_lines = []
    section_buffer = []
    
    def process_section():
        nonlocal section_buffer, merged_lines
        if not section_buffer:
            return
        
        merge_index = next((i for i, line in enumerate(section_buffer) if "[merge here]" in line), -1)
        
        if merge_index != -1:
            # Add content before [merge here]
            merged_lines.extend(section_buffer[:merge_index])
            
            # Find and add corresponding content from source
            match = re.search(f"{re.escape(current_heading)}(.*?)(?=\n#|$)", source_content, re.DOTALL)
            if match:
                merged_content = match.group(1).strip().split('\n')
                # Remove the heading if it's the first line of merged_content
                if merged_content and merged_content[0].startswith('#'):
                    merged_content = merged_content[1:]
                merged_lines.extend(merged_content)
            
            # Add content after [merge here]
            merged_lines.extend(section_buffer[merge_index+1:])
        else:
            # If no [merge here], add entire section
            merged_lines.extend(section_buffer)
        
        section_buffer.clear()

    for line in expanded_lines:
        if line.startswith('#'):
            process_section()
            current_heading = line
            section_buffer = [line]
        else:
            section_buffer.append(line)

    # Process the last section
    process_section()

    # Step 7: Save as merged doc
    with open(merged_file, 'w') as f:
        f.write('\n'.join(merged_lines))

    print(f"Merged document saved as: {merged_file}")

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