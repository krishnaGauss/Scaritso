# Website Knowledge Base Crawler

A modular Python system that crawls a website and converts all readable content into clean Markdown files. This tool is designed to build a knowledge base from web content, supporting both automatic crawling via sitemaps and manual URL lists.

## Features

- **Auto Mode**: Automatically detects sitemaps, discovers URLs, and crawls the entire site (with configurable limits).
- **Manual Mode**: Processes a specific list of URLs provided in a text file.
- **Content Extraction**: Uses `trafilatura` to extract main content, removing boilerplate like navbars, ads, and footers.
- **Markdown Conversion**: Converts HTML content to clean, formatted Markdown using `markdownify`.
- **Metadata**: Adds YAML frontmatter to each Markdown file with title, URL, and crawl timestamp.
- **Robustness**: Handles retries, timeouts, and user-agent rotation.

## System Architecture

![System Design](System%20Design.png)

The project is structured into modular components:

- **`main.py`**: CLI entry point and orchestrator.
- **`crawler/sitemap_parser.py`**: Detects and parses `sitemap.xml` and sitemap indexes.
- **`crawler/url_discovery.py`**: Normalizes URLs and handles fallbacks.
- **`crawler/fetcher.py`**: Fetches HTML with `requests`, handling retries and headers.
- **`crawler/extractor.py`**: Extracts clean content using `trafilatura`.
- **`crawler/markdown_converter.py`**: Converts content to Markdown.
- **`crawler/writer.py`**: Saves files to the `knowledge-base/` directory.

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Auto Mode
Crawl a website by providing its base URL. The system will look for a sitemap.
```bash
python main.py --auto https://example.com
```

Limit the number of pages:
```bash
python main.py --auto https://example.com --max 10
```

### Manual Mode
Process a list of URLs from a file (one URL per line).
```bash
python main.py --manual urls.txt
```

## Project Structure

```
website-kb-crawler/
│── crawler/
│    ├── __init__.py
│    ├── sitemap_parser.py
│    ├── url_discovery.py
│    ├── fetcher.py
│    ├── extractor.py
│    ├── markdown_converter.py
│    ├── writer.py
│── main.py
│── requirements.txt
│── README.md
```

## Future Enhancements

- **Async Crawling**: Use `aiohttp` for faster concurrent crawling.
- **Headless Browser**: Integrate `selenium` or `playwright` for JavaScript-heavy sites.
- **Respect robots.txt**: Add a parser to respect crawling rules.
- **Incremental Crawling**: Only crawl pages that have changed since the last run.
