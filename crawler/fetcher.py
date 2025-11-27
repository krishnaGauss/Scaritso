import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session():
    """
    Creates a requests session with retry logic.
    """
    session = requests.Session()
    retry = Retry(
        total=3,
        read=3,
        connect=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def fetch_url(url):
    """
    Fetches the HTML content of a URL.
    Returns the HTML string or None if failed.
    """
    session = create_session()
    headers = {
        'User-Agent': 'WebsiteKnowledgeBaseCrawler/1.0 (Python; +https://github.com/yourusername/website-kb-crawler)'
    }
    
    try:
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            print(f"Skipping non-HTML content: {url} ({content_type})")
            return None
            
        return response.text
        
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
