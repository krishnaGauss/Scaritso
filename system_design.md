# System Design: Website Knowledge Base Crawler

This document outlines the system architecture and data flow of the Website Knowledge Base Crawler.

## Data Flow Description

The data flow consists of six main stages:

### 1. Input & Discovery
- **Auto Mode**: The `SitemapParser` fetches `sitemap.xml` from the base URL. It parses the XML to extract all page URLs. If no sitemap is found, `URLDiscovery` generates common fallback URLs (e.g., `/about`, `/contact`).
- **Manual Mode**: The system reads a list of URLs from a user-provided text file.
- **Normalization**: `URLDiscovery` cleans all URLs (removing fragments, query params) and deduplicates them to ensure each page is processed only once.

### 2. Fetching
- **Input**: List of unique, normalized URLs.
- **Process**: The `Fetcher` iterates through the list. It uses a `requests.Session` with a custom `User-Agent` and retry logic (backoff strategy) to handle network instability or rate limits.
- **Output**: Raw HTML content of the page.

### 3. Extraction
- **Input**: Raw HTML.
- **Process**: The `Extractor` uses `trafilatura` to analyze the DOM. It identifies the "main" content by stripping away:
    - Navigation bars
    - Footers
    - Sidebars
    - Ads and popups
    - Cookie banners
- **Output**: Cleaned HTML/XML containing only the relevant article text, tables, and content links.

### 4. Conversion
- **Input**: Cleaned HTML/XML.
- **Process**: The `MarkdownConverter` uses `markdownify` to transform the markup into Markdown.
    - Converts `<h1>`-`<h6>` to `#`-`######`.
    - Converts `<a>` tags to `[text](url)`.
    - Converts `<table>` to Markdown tables.
    - Removes excessive newlines generated during conversion.
- **Output**: Clean Markdown text string.

### 5. Metadata Enrichment
- **Input**: Markdown text, Source URL.
- **Process**: The `Writer` prepares the file content. It generates a YAML frontmatter header containing:
    - `title`: Extracted from the content or URL.
    - `url`: The source URL.
    - `crawled_at`: Timestamp of execution.
- **Output**: Final file content string.

### 6. Storage
- **Process**: The `Writer` determines a safe filename from the URL path (replacing special characters with underscores). It handles filename collisions by appending a counter (e.g., `page_1.md`).
- **Action**: Writes the file to the `knowledge-base/` directory.

## Component Responsibilities

| Module | Responsibility | Key Libraries |
|--------|----------------|---------------|
| `main.py` | CLI interface, orchestration, progress tracking | `argparse`, `tqdm` |
| `sitemap_parser.py` | XML parsing, sitemap index handling | `xml.etree`, `requests` |
| `url_discovery.py` | URL normalization, filtering, fallbacks | `urllib.parse` |
| `fetcher.py` | HTTP requests, retries, user-agent | `requests`, `urllib3` |
| `extractor.py` | Content extraction, boilerplate removal | `trafilatura` |
| `markdown_converter.py` | HTML to Markdown conversion | `markdownify` |
| `writer.py` | File I/O, filename sanitization, metadata | `os`, `re` |
