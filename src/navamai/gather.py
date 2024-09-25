# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import os
import re
from urllib.parse import urljoin, urlparse

import html2text
import requests
from bs4 import BeautifulSoup
from markdown2 import Markdown
from readability import Document
from rich.progress import (BarColumn, Progress, SpinnerColumn, TaskID,
                           TextColumn)
from robotexclusionrulesparser import RobotExclusionRulesParser

import navamai.configure as configure


def article_scrape(
    url, progress: Progress, task_id: TaskID, save_folder, CUSTOM_USER_AGENT
):
    progress.update(task_id, description="Checking robots.txt", completed=5)
    rerp = RobotExclusionRulesParser()
    robots_url = urljoin(url, "/robots.txt")
    rerp.fetch(robots_url)
    if not rerp.is_allowed("*", url):
        progress.update(task_id, description="Scraping not allowed", completed=100)
        return None

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Create a session with custom headers
    session = requests.Session()
    session.headers.update({"User-Agent": CUSTOM_USER_AGENT})

    progress.update(task_id, description="Fetching webpage", completed=10)
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    progress.update(task_id, description="Extracting main content", completed=20)
    doc = Document(response.text)
    content = doc.summary()
    content_soup = BeautifulSoup(content, "html.parser")

    progress.update(task_id, description="Converting HTML to Markdown", completed=30)
    h = html2text.HTML2Text()
    h.body_width = 0
    markdown = h.handle(str(content_soup))

    progress.update(task_id, description="Processing images", completed=40)
    img_tags = content_soup.find_all("img")
    total_images = len(img_tags)

    for i, img in enumerate(img_tags, 1):
        img_url = urljoin(url, img.get("src"))
        img_name = os.path.basename(urlparse(img_url).path)
        img_path = os.path.join(save_folder + "/images", img_name)

        progress.update(
            task_id,
            description=f"Downloading image {i}/{total_images}",
            completed=40 + (i / total_images) * 40,
        )
        try:
            # Use the session with custom User-Agent for image downloads
            with session.get(img_url, stream=True) as r:
                r.raise_for_status()
                with open(img_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            # Replace image URL with local filename in markdown
            markdown = re.sub(
                r"!\[([^\]]*)\]\([^\)]*" + re.escape(img_name) + r"\)",
                f"![\\1]({'images/' + img_name})",
                markdown,
            )
        except requests.RequestException as e:
            print(f"Failed to download image {img_url}: {e}")

    progress.update(task_id, description="Determining file name", completed=90)
    # Try to get title from metadata, fallback to h1, then to url
    title = soup.find("meta", property="og:title") or soup.find(
        "meta", {"name": "title"}
    )
    if title:
        file_name = title.get("content")
    else:
        file_name = soup.find("h1")
        if file_name:
            file_name = file_name.text
        else:
            file_name = urlparse(url).path.split("/")[-1]

    # Clean the file name
    file_name = re.sub(r"[^\w\-_\. ]", "_", file_name)
    file_name = file_name.strip()
    if not file_name.endswith(".md"):
        file_name += ".md"
    file_path = os.path.join(save_folder, file_name)

    progress.update(task_id, description="Saving Markdown file", completed=95)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    progress.update(task_id, description="Scraping completed", completed=100)
    return file_path


def article(url):
    config = configure.load_config()
    gather_config = config.get("gather")

    # Define a custom User-Agent
    CUSTOM_USER_AGENT = f"{gather_config.get('user-agent')} ({gather_config.get('user-website')}; {gather_config.get('user-email')}) python-requests/2.26.0"
    save_folder = gather_config.get("save-folder")
    with Progress(
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task(description="Starting...", total=100)
        result = article_scrape(url, progress, task, save_folder, CUSTOM_USER_AGENT)
    return result
