import requests
from bs4 import BeautifulSoup
import sys
import logging
import random
import time
from urllib.parse import urlparse, quote
import os

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# List of common user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/120.0.0.0",
]

# Search engines
SEARCH_ENGINES = [
    {
        "name": "Baidu",
        "url": "https://www.baidu.com/s?wd={}&rn=50",
        "result_selector": "h3.t",
        "link_selector": "a"
    },
    {
        "name": "Sogou",
        "url": "https://www.sogou.com/web?query={}",
        "result_selector": "div.vrwrap",
        "link_selector": "h3.vr-title a"
    },
    {
        "name": "360",
        "url": "https://www.so.com/s?q={}",
        "result_selector": "h3.res-title",
        "link_selector": "a"
    }
]

def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.google.com/",
        "DNT": "1"
    }

def search_engine(company_name, section_title, file_number, engine):
    try:
        print(f"\nTrying {engine['name']} search for section {file_number}: {section_title}")
        
        # Construct search query
        query = f"{company_name} {section_title}"
        encoded_query = quote(query)
        url = engine['url'].format(encoded_query)
        
        # Get with retry
        for attempt in range(3):
            try:
                headers = get_headers()
                response = requests.get(
                    url, 
                    headers=headers, 
                    timeout=30,
                    allow_redirects=True
                )
                response.raise_for_status()
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == 2:
                    return False
                time.sleep(random.uniform(2, 5))
        
        # Parse results
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.select(engine['result_selector'])
        print(f"Found {len(results)} results from {engine['name']}")
        
        if not results:
            return False
        
        successful_contents = []
        
        # Process results
        for idx, result in enumerate(results[:10], 1):
            try:
                # Find link
                link = result.select_one(engine['link_selector'])
                if not link or not link.get('href'):
                    continue
                
                url = link['href']
                if not url.startswith('http'):
                    continue
                    
                print(f"Trying URL {idx}: {url}")
                
                # Get content with retry
                for attempt in range(2):
                    try:
                        content_response = requests.get(
                            url, 
                            headers=get_headers(), 
                            timeout=20,
                            allow_redirects=True
                        )
                        content_response.raise_for_status()
                        break
                    except:
                        if attempt == 1:
                            raise
                        time.sleep(random.uniform(1, 3))
                
                # Parse content
                content_soup = BeautifulSoup(content_response.content, "html.parser")
                
                # Remove unwanted elements
                for tag in content_soup.select('script, style, nav, header, footer, iframe'):
                    tag.decompose()
                
                text_content = content_soup.get_text(separator='\n', strip=True)
                
                if len(text_content) < 200:  # Increased minimum length
                    continue
                
                successful_contents.append(text_content)
                print(f"Successfully got content from URL {idx}")
                
                if len(successful_contents) >= 2:  # Get at least 2 sources
                    break
                    
            except Exception as e:
                print(f"Error processing result {idx}: {str(e)}")
                continue
            
            time.sleep(random.uniform(1, 2))
        
        if successful_contents:
            combined_content = "\n\n=== New Source ===\n\n".join(successful_contents)
            output_file = f"search{file_number}.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(combined_content)
            print(f"Saved content from {len(successful_contents)} sources")
            return True
            
        return False
        
    except Exception as e:
        print(f"Error in {engine['name']} search: {str(e)}")
        return False

def search_all_engines(company_name, section_title, file_number):
    for engine in SEARCH_ENGINES:
        try:
            if search_engine(company_name, section_title, file_number, engine):
                return True
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f"Error with {engine['name']}: {str(e)}")
            continue
    return False

def run_search(company_name):
    print(f"\nStarting search for: {company_name}")
    
    if not company_name:
        raise ValueError("Company name is required")
    
    try:
        # Read sections
        with open("table_of_content.txt", "r", encoding="utf-8") as f:
            content = f.read()
            sections = [line.strip() for line in content.splitlines() if line.strip()]
            
        if not sections:
            raise ValueError("No sections found in table_of_content.txt")
            
        print(f"Found {len(sections)} sections to search")
        
        # Process sections
        successful = 0
        for i, section in enumerate(sections, 1):
            # Clean section title
            if '. ' in section:
                section = section.split('. ', 1)[1]
            
            if search_all_engines(company_name, section, i):
                successful += 1
                print(f"Successfully processed section {i}")
            else:
                print(f"Failed to process section {i}")
            
            if i < len(sections):
                delay = random.uniform(3, 6)
                print(f"Waiting {delay:.1f} seconds before next section...")
                time.sleep(delay)
        
        print(f"\nSearch completed. Successful: {successful}/{len(sections)}")
        
        if successful > 0:
            return successful
        else:
            raise ValueError(f"No successful searches completed out of {len(sections)} sections")
            
    except Exception as e:
        print(f"Error in search process: {str(e)}")
        raise

if __name__ == "__main__":
    print("This script should be imported and run_search() should be called from main_GUI.py")