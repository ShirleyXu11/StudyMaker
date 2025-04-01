import os
import json
import requests
import shutil
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up the DeepSeek API client
base_url = "https://api.deepseek.com/v1"

def get_most_relevant_section(content, section_titles, api_key):
    prompt = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": f"""
             我需要将以下内容分类到以下章节标题之一：{', '.join(section_titles)}。
             请告诉我最相关的章节标题, 只需要告诉我标题编号（例如：1，2，3，...), 不要回复任何其他信息和文字。
             内容: {content}
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
                "Authorization": f"Bearer {api_key}"
            },
            data=json.dumps(prompt)
        )

        if response.status_code == 200:
            result = response.json().get("choices")[0].get("message").get("content")
            return result.strip()
        else:
            logging.error(f"Error checking relevance: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logging.error(f"Error processing content: {e}")
        return None

def process_file(filename, section_titles, section_to_folder, search_files_dir, api_key):
    # Read the content of the file with utf-8 encoding
    with open(os.path.join(search_files_dir, filename), 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Get the most relevant section title
    most_relevant_section = get_most_relevant_section(content, section_titles, api_key)
    
    if most_relevant_section is None:
        logging.error(f"Failed to classify content in file: {filename}")
        return

    # Determine the corresponding folder
    base_directory = os.getcwd()
    target_folder = os.path.join(base_directory, most_relevant_section)
    
    # Ensure the target folder exists
    if not os.path.exists(target_folder):
        logging.error(f"Target folder {target_folder} does not exist for file: {filename}")
        return

    # Print the target directory
    logging.info(f"Trying to move file {filename} to directory: {target_folder}")

    # Move the file to the corresponding folder
    try:
        shutil.move(os.path.join(search_files_dir, filename), os.path.join(target_folder, filename))
        logging.info(f"Moved file {filename} to folder {most_relevant_section}")
    except Exception as e:
        logging.error(f"Error moving file {filename} to folder {most_relevant_section}: {e}")

def process_files_parallel(files, section_titles, section_to_folder, search_files_dir, api_key, num_threads=40):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(process_file, filename, section_titles, section_to_folder, search_files_dir, api_key)
            for filename in files
        ]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error in future: {e}")

def main(company_name, api_key):
    try:
        # Read the table of contents with utf-8 encoding
        with open('table_of_content.txt', 'r', encoding='utf-8') as file:
            section_titles = [line.strip() for line in file.readlines()]

        # Create a dictionary to map section titles to folder numbers
        section_to_folder = {title: str(i+1) for i, title in enumerate(section_titles)}
        logging.info(f"Section to Folder Mapping: {section_to_folder}")

        # Directory containing the search files
        search_files_dir = os.getcwd()

        # List of files to process
        files_to_process = [
            filename for filename in os.listdir(search_files_dir) 
            if filename.startswith('search') and filename.endswith('.txt')
        ]

        # Process files in parallel with 40 threads
        process_files_parallel(
            files_to_process,
            section_titles,
            section_to_folder,
            search_files_dir,
            api_key,
            num_threads=40
        )

        return "Search3 completed successfully"
    except Exception as e:
        return f"Error in search3: {str(e)}"

if __name__ == "__main__":
    # For testing purposes
    import sys
    if len(sys.argv) > 2:
        result = main(sys.argv[1], sys.argv[2])
    else:
        result = main("test_company", "test_api_key")
    print(result)