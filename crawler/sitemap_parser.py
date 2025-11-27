import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin

def get_sitemap_urls(base_url):
    """
    Detects and parses sitemaps to extract all URLs.
    """
    common_sitemap_paths = [
        "/sitemap.xml",
        "/sitemap_index.xml",
        "/sitemap"
    ]
    
    found_urls = set()
    sitemap_url = None

    # 1. Detect Sitemap
    for path in common_sitemap_paths:
        test_url = urljoin(base_url, path)
        try:
            response = requests.get(test_url, timeout=10)
            if response.status_code == 200 and 'xml' in response.headers.get('Content-Type', ''):
                sitemap_url = test_url
                break
        except requests.RequestException:
            continue

    if not sitemap_url:
        print("No sitemap found.")
        return []

    print(f"Sitemap found at: {sitemap_url}")
    
    # 2. Parse Sitemap (Recursive for indexes)
    def parse_sitemap(url):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return

            try:
                root = ET.fromstring(response.content)
            except ET.ParseError:
                return

            # Check if it's a sitemap index
            # Namespace handling is often needed for sitemaps
            namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            
            # Look for <sitemap> tags (Sitemap Index)
            sitemaps = root.findall('ns:sitemap', namespaces)
            if not sitemaps:
                 # Fallback if namespace is missing or different
                 sitemaps = root.findall('sitemap')

            if sitemaps:
                for sm in sitemaps:
                    loc = sm.find('ns:loc', namespaces)
                    if loc is None:
                        loc = sm.find('loc')
                    if loc is not None and loc.text:
                        parse_sitemap(loc.text)
            else:
                # Look for <url> tags (Regular Sitemap)
                urls = root.findall('ns:url', namespaces)
                if not urls:
                    urls = root.findall('url')
                
                for u in urls:
                    loc = u.find('ns:loc', namespaces)
                    if loc is None:
                        loc = u.find('loc')
                    if loc is not None and loc.text:
                        found_urls.add(loc.text)

        except requests.RequestException:
            print(f"Failed to fetch sitemap: {url}")

    parse_sitemap(sitemap_url)
    return list(found_urls)
