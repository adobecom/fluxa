"""
Web article content extractor
"""

import re
from typing import Dict, Any
import requests
from bs4 import BeautifulSoup


class WebExtractor:
    """Extract tutorial content from web articles"""

    def __init__(self, timeout: int = 30):
        """
        Initialize web extractor
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/91.0.4472.124 Safari/537.36'
        }

    def extract(self, url: str, max_length: int = 100000) -> Dict[str, Any]:
        """
        Extract content from web article
        
        Args:
            url: Article URL
            max_length: Maximum content length
            
        Returns:
            Dictionary with content and metadata
            
        Raises:
            ValueError: If content cannot be extracted
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch URL {url}: {str(e)}")

        try:
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Remove script and style elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                element.decompose()
            
            # Try to find main content area
            main_content = None
            content_selectors = [
                'article',
                'main',
                '[role="main"]',
                '.post-content',
                '.article-content',
                '.entry-content',
                '.content',
            ]
            
            for selector in content_selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    break
            
            # Fallback to body if no main content found
            if not main_content:
                main_content = soup.body
            
            if not main_content:
                raise ValueError("Could not find any content in the page")
            
            # Extract text
            text = main_content.get_text(separator='\n', strip=True)
            
            # Clean up multiple newlines and whitespace
            text = re.sub(r'\n\s*\n', '\n\n', text)
            text = re.sub(r' +', ' ', text)
            
            # Truncate if too long
            if len(text) > max_length:
                text = text[:max_length] + "... [truncated]"
            
            # Extract title
            title = "Unknown"
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text(strip=True)
            
            # Extract headings for structure
            headings = [h.get_text(strip=True) for h in main_content.find_all(['h1', 'h2', 'h3'])]
            
            return {
                "content": text,
                "source": url,
                "title": title,
                "type": "web",
                "headings": headings[:20],  # Limit to first 20 headings
            }
            
        except Exception as e:
            raise ValueError(f"Error parsing web content: {str(e)}")


