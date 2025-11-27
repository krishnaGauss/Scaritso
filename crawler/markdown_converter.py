from markdownify import markdownify as md

def to_markdown(content):
    """
    Converts HTML/XML content to Markdown.
    Ensures ATX-style headings and cleans excessive whitespace.
    """
    if not content:
        return ""

    # Convert to Markdown
    # heading_style="ATX" ensures #, ##, ###
    markdown_text = md(content, heading_style="ATX")
    
    # Clean excessive whitespace
    # markdownify sometimes leaves multiple newlines
    lines = markdown_text.splitlines()
    cleaned_lines = []
    for line in lines:
        if line.strip():
            cleaned_lines.append(line)
        else:
            # Keep max one empty line
            if cleaned_lines and cleaned_lines[-1].strip():
                cleaned_lines.append("")
                
    return "\n".join(cleaned_lines).strip()
