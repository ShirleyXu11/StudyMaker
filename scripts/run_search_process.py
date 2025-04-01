import sys
import os
import importlib
import logging

def run_search_process(company_name, api_key):
    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Define the sequence of scripts to run
    scripts = [
        ("search1", "Processing initial search files"),
        ("search1_create_folder", "Creating folders for sections"),
        ("search2", "Processing search results with DeepSeek API"),
        ("search3", "Organizing search results"),
        ("search4", "Finalizing search results")
    ]
    
    results = []
    
    for script_name, description in scripts:
        try:
            logging.info(f"Starting {description}")
            # Import the module dynamically
            module = importlib.import_module(script_name)
            
            # Call the main function with required parameters
            if hasattr(module, 'main'):
                result = module.main(company_name, api_key)
                results.append(f"{script_name}: {result}")
            else:
                error_msg = f"{script_name}: No main function found"
                logging.error(error_msg)
                results.append(error_msg)
            
        except ImportError as e:
            error_msg = f"Error importing {script_name}: {str(e)}"
            logging.error(error_msg)
            results.append(error_msg)
        except Exception as e:
            error_msg = f"Error executing {script_name}: {str(e)}"
            logging.error(error_msg)
            results.append(error_msg)
    
    return "\n".join(results)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python run_search_process.py <company_name> <api_key>")
        sys.exit(1)
    
    company_name = sys.argv[1]
    api_key = sys.argv[2]
    result = run_search_process(company_name, api_key)
    print(result)
