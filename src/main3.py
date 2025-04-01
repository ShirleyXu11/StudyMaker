import json
import requests
import sys
import os
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

def main(company_name, user_demand):
    try:
        # Check if output.txt exists
        if not os.path.exists("output.txt"):
            raise Exception("Please generate document first (output.txt not found)")

        logging.info(f"Starting first revision for {company_name}")
        
        # Read the content
        with open("output.txt", "r", encoding="utf-8") as file:
            content = file.read()

        if not content:
            raise Exception("output.txt is empty")

        # Save the content back (in this version, we're just passing through)
        # In a real implementation, you might want to add revision logic here
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(content)
            
        logging.info(f"Completed first revision for {company_name}")
        return f"Successfully completed first revision for {company_name}"

    except Exception as e:
        error_msg = f"Error in first revision process: {str(e)}"
        logging.error(error_msg)
        raise Exception(error_msg)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error("Usage: python main3.py <company_name> [user_demand]")
        sys.exit(1)
    
    company_name = sys.argv[1]
    user_demand = sys.argv[2] if len(sys.argv) > 2 else ""
    
    try:
        result = main(company_name, user_demand)
        print(result)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)