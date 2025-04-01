import sys
import os
import subprocess

def run_search_initial(company_name, api_key):
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "search0.py")
    
    try:
        process = subprocess.Popen(
            ["python", script_path, company_name, api_key],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        
        print(stdout)
        if stderr:
            print(f"Error: {stderr}", file=sys.stderr)
    except Exception as e:
        print(f"Error executing search0.py: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python run_search_initial.py <company_name> <api_key>")
        sys.exit(1)
    
    company_name = sys.argv[1]
    api_key = sys.argv[2]
    run_search_initial(company_name, api_key)
