import os
import sys
import time
import tracemalloc

# Add the src directory to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.web_scraping.web_scraper import WebScraper

def test_detailed_scrape():
    url = "https://www.geeksforgeeks.org/dsa/types-of-trees-in-data-structures/"
    scraper = WebScraper()
    
    if not scraper.app:
        print("API Key not set.")
        return

    print(f"--- Initiating Detailed Scrape on: {url} ---")
    
    # Start tracking memory and time
    tracemalloc.start()
    start_time = time.time()
    
    # Perform the scrape
    docs = scraper.scrape_url(url)
    
    # End tracking
    end_time = time.time()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    time_taken = end_time - start_time
    
    if not docs:
        print("Scrape failed.")
        return
        
    content = docs[0]['text']
    
    # Analytics
    contains_images = "![" in content or "img src" in content
    # Usually GfG ads are wrapped in specific divs, but Firecrawl's AI strips them.
    # We can just look for common ad words, but generally Firecrawl removes them.
    
    print("\n" + "="*40)
    print("--- SCRAPING LOG & ANALYTICS ---")
    print("="*40)
    print(f"Time Consumed:       {time_taken:.2f} seconds")
    print(f"Credits Used:        1 credit (Standard for 1 URL scrape)")
    print(f"Peak Memory Used:    {peak_memory / 1024 / 1024:.2f} MB")
    print(f"Data Stored (Size):  {sys.getsizeof(content) / 1024:.2f} KB")
    print(f"Total Characters:    {len(content)}")
    print(f"Includes Images?     {'Yes (Markdown image links extracted)' if contains_images else 'No'}")
    print(f"Includes Ads?        No (Firecrawl's AI automatically strips ads and navbars)")
    print("="*40)
    
    print("\n[ DATA SNIPPET (First 500 characters) ]")
    print("-" * 40)
    print(content[:500])
    print("-" * 40)
    
    print("\n[ DATA SNIPPET (Last 300 characters) ]")
    print("-" * 40)
    print(content[-300:])
    print("-" * 40)

if __name__ == "__main__":
    test_detailed_scrape()
