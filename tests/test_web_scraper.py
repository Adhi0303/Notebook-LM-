import os
import sys

# Add the src directory to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.web_scraping.web_scraper import WebScraper

def test_web_scraper():
    print("--- Testing WebScraper ---")
    scraper = WebScraper()
    
    if not scraper.app:
        print("\nSkipping test because FIRECRAWL_API_KEY is not set.")
        return
        
    # We use a tiny, standard website to minimize token/credit usage
    test_url = "https://example.com"
    
    print("\n1. Testing Firecrawl scrape on a minimal site...")
    docs = scraper.scrape_url(test_url)
    
    print(f"\nExtracted docs: {len(docs)}")
    if len(docs) > 0:
        print(f"Metadata: {docs[0]['metadata']}")
        print(f"Content Snippet (first 100 chars):\n{docs[0]['text'][:100]}...\n")
        
        assert docs[0]['metadata']['source'] == test_url
        assert docs[0]['metadata']['type'] == "web"
        assert len(docs[0]['text']) > 10 # ensure we got some text back
        print("[PASS] Web scraping test passed successfully!")
    else:
        print("[FAIL] Failed to extract content.")

if __name__ == "__main__":
    test_web_scraper()
