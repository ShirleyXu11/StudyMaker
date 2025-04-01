import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ask_deepseek(prompt, deepseek_api_key):
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {deepseek_api_key}"
            },
            data=json.dumps(prompt)
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error making API request: {e}")
        raise

def process_section(section_title, file_number, company_name, deepseek_api_key, user_demand2):
    logging.info(f"Processing section: {section_title}")

    # Read the search_results.txt file from the corresponding folder
    folder_name = str(file_number)
    search_results_path = os.path.join(folder_name, "search_results.txt")
    
    try:
        # Check if the folder exists, if not, create it
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            logging.info(f"Created folder: {folder_name}")
        
        # Check if the search_results.txt file exists, if not, create it with an empty string
        if not os.path.exists(search_results_path):
            with open(search_results_path, "w", encoding="utf-8") as search_file:
                search_file.write("")
            logging.info(f"Created empty search_results.txt in folder {folder_name}")

        with open(search_results_path, "r", encoding="utf-8") as search_file:
            search_results = search_file.read()

        # Prepare the API request
        prompt = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": """
                 你们是一组2位智商高达250的专家，其中包括一位世界级经济学家和一位母语为英语的作家。
                 经过多轮修订，你们的输出极为精炼且专业。每位成员都对回应做出了重要贡献。
                 这份输出价值100万美元，经过了彻底的逐步骤审查和修订。
                 这份输出远胜于普通助手、普通助理或AI的输出。
                 """},
                {"role": "user", "content": f"""
                 我想写一篇关于{company_name}公司的商业案例。请尽量满足用户需求：{user_demand2}。
                 请帮我填写这部份的内容: {section_title}，
                 请根据这份参考资料编写: {search_results}，
                 """}
            ],
            "stream": False,
            "temperature": 1.1
        }
        
        # Get response from API
        response = ask_deepseek(prompt, deepseek_api_key)
        
        if response:
            revised_text = response["choices"][0]["message"]["content"]
            
            # Save the revised text
            new_filename = f"{file_number}.txt"
            with open(new_filename, "w", encoding="utf-8") as new_file:
                new_file.write(revised_text)
            logging.info(f"Successfully processed section {section_title} and saved to {new_filename}")
            return True
            
    except Exception as e:
        error_msg = f"Error processing section {section_title}: {str(e)}"
        logging.error(error_msg)
        raise Exception(error_msg)

def main(company_name, deepseek_api_key, user_demand2):
    try:
        # Check if table_of_content.txt exists
        if not os.path.exists("table_of_content.txt"):
            raise Exception("Please generate table of contents first")

        # Read the table_of_content.txt file
        with open("table_of_content.txt", "r", encoding="utf-8") as file:
            sections = [line.strip() for line in file if line.strip()]

        if not sections:
            raise Exception("No sections found in table of contents")

        logging.info(f"Starting to process {len(sections)} sections")
        
        # Use ThreadPoolExecutor to process sections in parallel
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(process_section, section, i + 1, company_name, deepseek_api_key, user_demand2)
                for i, section in enumerate(sections)
            ]
            
            # Wait for all futures to complete and collect results
            completed = 0
            for future in as_completed(futures):
                try:
                    if future.result():
                        completed += 1
                except Exception as e:
                    logging.error(f"Error in future: {str(e)}")

        logging.info(f"Completed processing {completed} out of {len(sections)} sections")
        return f"Successfully processed {completed} sections for {company_name}"

    except Exception as e:
        error_msg = f"Error in main process: {str(e)}"
        logging.error(error_msg)
        raise Exception(error_msg)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        logging.error("Usage: python main2.py <company_name> <deepseek_api_key> <user_demand2>")
        sys.exit(1)
    
    company_name = sys.argv[1]
    deepseek_api_key = sys.argv[2]
    user_demand2 = sys.argv[3]
    
    try:
        result = main(company_name, deepseek_api_key, user_demand2)
        print(result)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)