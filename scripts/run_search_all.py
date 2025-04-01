import subprocess
import logging
import sys
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get the absolute path of a script file
def get_script_path(script_name):
    if getattr(sys, 'frozen', False):
        # If the script is run as an executable, use sys._MEIPASS
        base_path = sys._MEIPASS
    else:
        # If the script is run as a regular Python file, use the script's directory
        base_path = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_path, script_name)
    return script_path

# Get the company name and API key from command-line arguments
if len(sys.argv) < 3:
    logging.error("Usage: python run_search_all.py <company_name> <deepseek_api_key>")
    sys.exit(1)

company_name = sys.argv[1]
deepseek_api_key = sys.argv[2]

print(f"Received Company Name: {company_name}")  # Debugging print statement

# Construct the full paths to the search scripts
search0_path = get_script_path("search0.py")
search1_path = get_script_path("search1.py")
search1_create_folder_path = get_script_path("search1_create_folder.py")
search2_path = get_script_path("search2.py")
search3_path = get_script_path("search3.py")
search4_path = get_script_path("search4.py")

files_to_run = [
    ["python", search0_path, company_name],
    ["python", search1_path],
    ["python", search1_create_folder_path],
    ["python", search2_path, company_name, deepseek_api_key],
    ["python", search3_path],
    ["python", search4_path]
]

for file in files_to_run:
    try:
        logging.info(f"Running {file}")
        result = subprocess.run(file, check=True, capture_output=True, text=True)
        logging.info(f"Successfully ran {file}")
        logging.info(f"Output:\n{result.stdout}")
        if result.stderr:
            logging.warning(f"Error output:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to run {file}: {e}")
        logging.error(f"Error output:\n{e.stderr}")
        break  # Stop execution if a file fails