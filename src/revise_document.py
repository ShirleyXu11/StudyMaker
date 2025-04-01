import os
import sys
import json
import requests
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def call_deepseek(prompt, api_key):
    try:
        base_url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 1.1
        }
        response = requests.post(base_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"API call error: {str(e)}")
        raise

def revise_single_document(file_name, revision_demand, api_key):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()

        prompt = f"Please revise the following text based on this demand: {revision_demand}\n\nOriginal text:\n{content}"
        response = call_deepseek(prompt, api_key)

        if "choices" in response and len(response["choices"]) > 0:
            revised_content = response["choices"][0]["message"]["content"]

            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(revised_content)

            logging.info(f"Successfully revised {file_name}")
            return True
        else:
            raise Exception(f"Invalid API response for {file_name}")
            
    except Exception as e:
        logging.error(f"Error processing {file_name}: {str(e)}")
        raise

def revise_document(company_name, api_key, revision_demand):
    try:
        txt_files = [f for f in os.listdir() if f.endswith('.txt') and f[0].isdigit()]
        if not txt_files:
            raise Exception("No text files found to revise")
            
        txt_files.sort(key=lambda x: int(x.split('.')[0]))
        logging.info(f"Found {len(txt_files)} files to revise")

        completed = 0
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(revise_single_document, file_name, revision_demand, api_key): file_name 
                for file_name in txt_files
            }
            
            for future in as_completed(futures):
                try:
                    if future.result():
                        completed += 1
                except Exception as e:
                    logging.error(f"Error in revision: {str(e)}")

        result = f"Successfully revised {completed} out of {len(txt_files)} sections"
        logging.info(result)
        return result

    except Exception as e:
        error_msg = f"Error in document revision: {str(e)}"
        logging.error(error_msg)
        raise Exception(error_msg)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python revise_document.py <company_name> <api_key> <revision_demand>")
        sys.exit(1)

    company_name = sys.argv[1]
    api_key = sys.argv[2]
    revision_demand = sys.argv[3]
    
    try:
        result = revise_document(company_name, api_key, revision_demand)
        print(result)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
