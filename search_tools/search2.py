import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

base_url = "https://api.deepseek.com/v1"

def is_relevant(file_path, company_name, deepseek_api_key):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return None

    prompt = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": f"""
             我需要写作一份{company_name}案例研究。
             提取所有对写这份案例研究有用的资料，并按原文保留下来。
             不要新加入材料，也不要回复任何检查内容以外的信息，无关的资料请帮忙删掉。
             如果这段内容没有相关的内容，请直接回答"No"。 
             检查内容: {content}
             """}
        ],
        "stream": False,
        "temperature": 1.1
    }
             
    logging.debug(json.dumps(prompt, indent=4, ensure_ascii=False))  # Log the prompt

    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {deepseek_api_key}"
            },
            data=json.dumps(prompt)
        )

        if response.status_code == 200:
            result = response.json().get("choices")[0].get("message").get("content")
            return result
        else:
            logging.error(f"Error checking relevance: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
        return None

def process_file(file_path, company_name, deepseek_api_key):
    relevant_content = is_relevant(file_path, company_name, deepseek_api_key)
    
    if relevant_content is not None:
        if "no" in relevant_content.lower():
            logging.info(f"No relevant content found in: {file_path}")
            try:
                os.remove(file_path)  # Remove the file if it's not relevant
                logging.info(f"Removed input file: {file_path}")
            except Exception as e:
                logging.error(f"Error removing file {file_path}: {e}")
        else:
            # Replace the original file with the relevant content
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(relevant_content)
                logging.info(f"Replaced original file with relevant content: {file_path}")
            except Exception as e:
                logging.error(f"Error writing to file {file_path}: {e}")

def process_files_parallel(files, company_name, deepseek_api_key, num_threads=40):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(process_file, file, company_name, deepseek_api_key) 
            for file in files
        ]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error in future: {e}")

def main(company_name, api_key):
    try:
        folder_path = os.path.dirname(os.path.abspath(__file__))
        files = [
            os.path.join(folder_path, filename) 
            for filename in os.listdir(folder_path) 
            if filename.startswith("search") and filename.endswith(".txt")
        ]
        
        # Sort files
        files.sort(key=lambda x: tuple(map(lambda y: int(y) if y.isdigit() else y, 
                                         os.path.basename(x).replace('.txt', '').split('_'))))
        
        # Process files in parallel with 40 threads
        process_files_parallel(files, company_name, api_key, num_threads=40)
        
        return "Search2 completed successfully"
    except Exception as e:
        return f"Error in search2: {str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("company_name", help="Company name to search for")
    parser.add_argument("deepseek_api_key", help="DeepSeek API key")
    args = parser.parse_args()

    company_name = args.company_name
    deepseek_api_key = args.deepseek_api_key
    result = main(company_name, deepseek_api_key)
    print(result)