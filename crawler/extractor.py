import trafilatura

def extract_content(html):
    """
    Extracts the main content from the HTML using trafilatura.
    Preserves tables and links.
    """
    if not html:
        return None
        
    # include_tables=True, include_links=True are important options
    # We use output_format='xml' so we can pass it to markdownify later
    extracted_content = trafilatura.extract(
        html,
        include_tables=True,
        include_links=True,
        include_images=False,
        include_comments=False,
        output_format='xml',
        no_fallback=False
    )
    
    return extracted_content
