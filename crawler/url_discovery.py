from urllib.parse import urlparse, urljoin

def normalize_url(url):
    """
    Normalizes a URL by removing fragments and query parameters (optional).
    Ensures it ends without a slash for consistency, or with one, but we'll choose without.
    """
    parsed = urlparse(url)
    # Reconstruct without fragment
    normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return normalized

def filter_urls(urls, base_domain):
    """
    Filters URLs to ensure they belong to the base domain.
    """
    valid_urls = set()
    base_netloc = urlparse(base_domain).netloc
    
    for url in urls:
        normalized = normalize_url(url)
        parsed = urlparse(normalized)
        if parsed.netloc == base_netloc or parsed.netloc.endswith("." + base_netloc):
             valid_urls.add(normalized)
    
    return list(valid_urls)

def get_fallback_urls(base_url):
    """
    Returns a list of common fallback URLs if no sitemap is found.
    """
    paths = [
        "",
        "about",
        "blog",
        "docs",
        "contact",
        "products",
        "services"
    ]
    
    return [urljoin(base_url, path) for path in paths]
