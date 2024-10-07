## Article Scraper

This Streamlit app provides a user-friendly interface for scraping web articles and saving them as markdown files. It utilizes the `navamai.gather` module to perform the scraping functionality.

## Install script

```bash
#!/bin/bash

# Create and navigate to the app directory
mkdir article_scraper
cd article_scraper

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install streamlit navamai requests beautifulsoup4 html2text readability-lxml robotexclusionrulesparser markdown2 rich

# Create the main.py file
touch main.py
```

## File: main.py

```python
import streamlit as st
import navamai.gather as gather
import navamai.configure as configure
import os
from urllib.parse import urlparse
import re

st.set_page_config(page_title="Article Scraper", layout="wide")

st.title("Article Scraper")

st.sidebar.header("Configuration")
save_folder = st.sidebar.text_input("Save Folder", value=configure.load_config().get("gather", {}).get("save-folder", ""))
user_agent = st.sidebar.text_input("User Agent", value=configure.load_config().get("gather", {}).get("user-agent", ""))
user_website = st.sidebar.text_input("User Website", value=configure.load_config().get("gather", {}).get("user-website", ""))
user_email = st.sidebar.text_input("User Email", value=configure.load_config().get("gather", {}).get("user-email", ""))

if st.sidebar.button("Save Configuration"):
    config = configure.load_config()
    config["gather"] = {
        "save-folder": save_folder,
        "user-agent": user_agent,
        "user-website": user_website,
        "user-email": user_email
    }
    configure.save_config(config)
    st.sidebar.success("Configuration saved successfully!")

url = st.text_input("Enter the URL of the article to scrape:")

def update_image_paths(content, save_folder):
    def replace_path(match):
        old_path = match.group(1)
        images_folder = os.path.join(save_folder, "images")
        new_path = os.path.join(images_folder, os.path.basename(old_path))
        return f"({new_path})"
    
    return re.sub(r'\((.*?)\)', replace_path, content)

if st.button("Scrape Article"):
    if url:
        with st.spinner("Scraping article..."):
            # Create save_folder and images subfolder if they don't exist
            if save_folder:
                os.makedirs(save_folder, exist_ok=True)
                os.makedirs(os.path.join(save_folder, "images"), exist_ok=True)
            
            result = gather.article(url)
        
        if result:
            st.success(f"Article scraped successfully! Saved to: {result}")
            
            # Update image paths in the markdown file
            with open(result, "r", encoding="utf-8") as f:
                content = f.read()
            
            updated_content = update_image_paths(content, save_folder)
            
            with open(result, "w", encoding="utf-8") as f:
                f.write(updated_content)
            
            # Display updated article content
            st.markdown(updated_content)
            
            # Display images
            st.subheader("Images")
            images_folder = os.path.join(save_folder, "images")
            if os.path.exists(images_folder):
                for img in os.listdir(images_folder):
                    img_path = os.path.join(images_folder, img)
                    if os.path.isfile(img_path):
                        st.image(img_path, caption=img, use_column_width=True)
                    else:
                        st.warning(f"Image not found: {img_path}")
            else:
                st.info("No images found for this article.")
        else:
            st.error("Failed to scrape the article. Please check the URL and try again.")
    else:
        st.warning("Please enter a URL to scrape.")

# Display recent scrapes
st.sidebar.header("Recent Scrapes")
if save_folder and os.path.exists(save_folder):
    files = sorted([f for f in os.listdir(save_folder) if f.endswith('.md')], key=lambda x: os.path.getmtime(os.path.join(save_folder, x)), reverse=True)
    for file in files[:5]:
        if st.sidebar.button(file):
            with open(os.path.join(save_folder, file), "r", encoding="utf-8") as f:
                content = f.read()
            st.markdown(content)
else:
    st.sidebar.info("No recent scrapes found.")
```

## Run script

```bash
#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Run the Streamlit app
streamlit run main.py
```
