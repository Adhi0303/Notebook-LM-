"""
Web Scraper Module
Handles website content extraction using Firecrawl.
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from firecrawl import FirecrawlApp

class WebScraper:
    def __init__(self):
        # Load environment variables from .env
        load_dotenv()
        
        # Initialize Firecrawl SDK
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            print("Warning: FIRECRAWL_API_KEY is not set. Web scraping will fail.")
            self.app = None
        else:
            self.app = FirecrawlApp(api_key=api_key)

    def scrape_url(self, url: str) -> List[Dict[str, Any]]:
        """
        Scrapes a URL using Firecrawl and returns the extracted Markdown content.
        The return format is identical to DocumentProcessor for pipeline consistency.
        """
        if not self.app:
            return []
            
        try:
            print(f"Scraping URL: {url}...")
            
            # Use Firecrawl to extract markdown
            scrape_result = self.app.scrape_url(url)
            
            # Firecrawl returns a Document object in v2+
            markdown_content = getattr(scrape_result, 'markdown', '')
            
            if not markdown_content.strip():
                print(f"Warning: No content extracted from {url}")
                return []
                
            # Wrap the content in our standard document format
            return [{
                "text": markdown_content.strip(),
                "metadata": {
                    "source": url,
                    "page": 1,
                    "type": "web"
                }
            }]
            
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return []
