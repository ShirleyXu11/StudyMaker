import logging
import sys
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(company_name, api_key, user_demand):
    try:
        logging.info(f"Starting process for company: {company_name}")
        
        # Import main1 functionality
        import main1
        
        # Call the main function from main1
        main1.main(company_name, api_key, user_demand)
        
        # Read the generated file
        try:
            with open("table_of_content.txt", "r", encoding="utf-8") as file:
                content = file.read()
            return f"Successfully generated table of contents for {company_name}:\n\n{content}"
        except FileNotFoundError:
            return f"Process completed but no output file was found for {company_name}"
        
    except Exception as e:
        error_msg = f"Error in run_main1: {str(e)}"
        logging.error(error_msg)
        return error_msg

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python run_main1.py <company_name> <api_key> [user_demand]")
        sys.exit(1)
        
    company_name = sys.argv[1]
    api_key = sys.argv[2]
    user_demand = sys.argv[3] if len(sys.argv) > 3 else ""
    
    result = main(company_name, api_key, user_demand)
    print(result)