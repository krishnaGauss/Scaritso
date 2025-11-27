import argparse
import sys
from tqdm import tqdm
from crawler import sitemap_parser, url_discovery, fetcher, extractor, markdown_converter, writer

def process_url(url):
    """
    Orchestrates the processing of a single URL.
    Returns the path of the saved file or None if failed.
    """
    html = fetcher.fetch_url(url)
    if not html:
        return None
        
    content = extractor.extract_content(html)
    if not content:
        # Try fallback or just skip
        return None
        
    markdown = markdown_converter.to_markdown(content)
    if not markdown:
        return None
        
    filepath = writer.save_file(url, markdown)
    return filepath

def auto_mode(base_url, max_pages):
    print(f"Starting Auto Mode for: {base_url}")
    
    # 1. Discover URLs
    urls = sitemap_parser.get_sitemap_urls(base_url)
    if not urls:
        print("No sitemap found. Using fallback URLs.")
        urls = url_discovery.get_fallback_urls(base_url)
    
    # Filter and Deduplicate
    urls = url_discovery.filter_urls(urls, base_url)
    
    # Limit
    if max_pages and len(urls) > max_pages:
        print(f"Limiting to {max_pages} pages (found {len(urls)}).")
        urls = urls[:max_pages]
    else:
        print(f"Found {len(urls)} pages to crawl.")

    success_count = 0
    with tqdm(total=len(urls)) as pbar:
        for url in urls:
            pbar.set_description(f"Processing {url}")
            filepath = process_url(url)
            if filepath:
                success_count += 1
            pbar.update(1)

    print(f"\nCompleted! Successfully saved {success_count}/{len(urls)} pages to 'knowledge-base/'.")

def manual_mode(file_path):
    print(f"Starting Manual Mode with file: {file_path}")
    
    try:
        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return

    # Normalize
    urls = [url_discovery.normalize_url(u) for u in urls]
    print(f"Found {len(urls)} URLs to process.")

    success_count = 0
    with tqdm(total=len(urls)) as pbar:
        for url in urls:
            pbar.set_description(f"Processing {url}")
            filepath = process_url(url)
            if filepath:
                success_count += 1
            pbar.update(1)

    print(f"\nCompleted! Successfully saved {success_count}/{len(urls)} pages to 'knowledge-base/'.")

def main():
    parser = argparse.ArgumentParser(description="Website Knowledge Base Crawler")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--auto", help="Base URL for auto-discovery mode")
    group.add_argument("--manual", help="Path to a text file containing URLs")
    
    parser.add_argument("--max", type=int, help="Maximum number of pages to crawl (Auto mode only)")
    
    args = parser.parse_args()

    if args.auto:
        auto_mode(args.auto, args.max)
    elif args.manual:
        manual_mode(args.manual)

if __name__ == "__main__":
    main()
