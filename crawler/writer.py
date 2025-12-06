import os
import re
from datetime import datetime
from urllib.parse import urlparse

def get_safe_filename(url):
    """
    Converts a URL into a safe filename.
    """
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if not path:
        filename = "index"
    else:
        filename = re.sub(r'[^a-zA-Z0-9]', '_', path)
    
    # Ensure unique filenames if needed, but for now just basic mapping
    return f"{filename}.md"

def save_file(url, content, ai_metadata=None, output_dir="knowledge-base"):
    """
    Saves the content to a markdown file with metadata.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = get_safe_filename(url)
    filepath = os.path.join(output_dir, filename)
    
    # Handle filename collisions (simple append)
    counter = 1
    base_filepath = filepath
    while os.path.exists(filepath):
        name, ext = os.path.splitext(base_filepath)
        filepath = f"{name}_{counter}{ext}"
        counter += 1

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Extract a simple title from content or URL
    # (Here we just use the URL as title for metadata, 
    # real title extraction would require parsing the HTML title tag which we might have lost)
    # But we can try to find the first header in the markdown
    title = url
    lines = content.splitlines()
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break

    # Format AI metadata for frontmatter
    ai_frontmatter = ""
    if ai_metadata:
        ai_frontmatter = f"""
ai_summary: "{ai_metadata.get('summary', '').replace('"', "'")}"
ai_tags: {ai_metadata.get('tags', [])}
ai_score: {ai_metadata.get('score', 0)}"""

    metadata = f"""---
title: {title}
url: {url}
crawled_at: {timestamp}{ai_frontmatter}
---

"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(metadata + content)
        
    return filepath
