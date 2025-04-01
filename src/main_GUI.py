import tkinter as tk
from tkinter import messagebox, font, scrolledtext
import subprocess
import os
import sys
import logging

# Add this block at the start
def prevent_multiple_instances():
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('localhost', 12346))
    except socket.error:
        messagebox.showwarning("Warning", "Application is already running!")
        sys.exit()
    return sock

# Call this function before creating the main window
sock = prevent_multiple_instances()

print("Python executable:", sys.executable)
print("Current working directory:", os.getcwd())


# 配置日志记录
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get the absolute path of a script file
def get_script_path(script_name):
    if getattr(sys, 'frozen', False):
        # If the script is run as an executable, use sys._MEIPASS
        base_path = sys._MEIPASS
    else:
        # If the script is run as a regular Python file, use the script's directory
        base_path = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_path, script_name)
    logging.debug(f"Script path: {script_path}")  # Print the path for debugging
    return script_path

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Placeholder functions for the buttons
def generate_table_of_content():
    logging.info("Generating Table of Content")
    company_name = entry.get()
    api_key = api_entry.get()
    user_demand1 = demand_text.get("1.0", tk.END).strip()
    
    if company_name and api_key:
        try:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Generating Table of Content for {company_name}...\n")
            root.update()  # Update the GUI to show the message
            
            # Import the module
            import run_main1
            
            # Run the main function
            result = run_main1.main(company_name, api_key, user_demand1)
            
            # Display result
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, str(result))
            logging.info(f"Completed: {result}")
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, error_msg)
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)
    else:
        messagebox.showwarning("Input Error", "Please enter a company name and API key.")
        logging.warning("Input Error: Company name or API key missing")

def search_internet():
    logging.info("Searching the internet")
    company_name = entry.get()
    api_key = api_entry.get()
    if company_name and api_key:
        try:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Searching the internet for resources related to {company_name}\n")
            root.update()
            
            # Check working directory and files
            current_dir = os.getcwd()
            output_text.insert(tk.END, f"\nWorking directory: {current_dir}\n")
            
            table_path = os.path.join(current_dir, "table_of_content.txt")
            if not os.path.exists(table_path):
                error_msg = f"Table of contents file not found at {table_path}.\nPlease generate table of contents first."
                output_text.insert(tk.END, f"\nError: {error_msg}")
                messagebox.showwarning("Warning", error_msg)
                return
            
            # Try to read and display file content
            try:
                with open(table_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    output_text.insert(tk.END, f"\nFound table of contents:\n{content}\n")
                    
                # Process the content into sections
                sections = []
                for line in content.splitlines():
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Remove any leading numbers and dots
                        cleaned_line = '.'.join(line.split('.')[1:]).strip() if '.' in line else line
                        if cleaned_line:
                            sections.append(cleaned_line)
                
                output_text.insert(tk.END, f"\nProcessed sections ({len(sections)}):\n")
                for i, section in enumerate(sections, 1):
                    output_text.insert(tk.END, f"{i}. {section}\n")
                root.update()
                
                if not sections:
                    raise ValueError("No valid sections found in table_of_content.txt")
                
            except Exception as e:
                error_msg = f"Error processing table of contents: {str(e)}"
                output_text.insert(tk.END, f"\nError: {error_msg}")
                messagebox.showerror("Error", error_msg)
                return
            
            # Import and use search0 module
            import search0
            result = search0.run_search(company_name)
            
            if result > 0:
                output_text.insert(tk.END, f"\nSearch completed successfully. Found content for {result} sections.")
            else:
                output_text.insert(tk.END, "\nSearch completed but no results were found.")
            
            logging.info(f"Search completed with {result} results")
            
        except Exception as e:
            error_msg = f"Error during search: {str(e)}"
            output_text.insert(tk.END, f"\nError: {error_msg}")
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)
    else:
        messagebox.showwarning("Input Error", "Please enter a company name and API key.")
        logging.warning("Input Error: Company name or API key missing")

def process_search_results():
    logging.info("Processing search results")
    company_name = entry.get()
    api_key = api_entry.get()
    if company_name and api_key:
        try:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Processing search results for {company_name}\n")
            root.update()
            
            # Import and run the search process
            import run_search_process
            result = run_search_process.run_search_process(company_name, api_key)
            
            # Display result
            output_text.insert(tk.END, "\nSearch results processing completed successfully")
            
            # If there's any output to display
            if isinstance(result, str):
                output_text.insert(tk.END, f"\nOutput:\n{result}")
            
            logging.info("Search processing completed successfully")
                
        except Exception as e:
            error_msg = f"Error processing search results: {str(e)}"
            output_text.insert(tk.END, f"\n{error_msg}")
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)
    else:
        messagebox.showwarning("Input Error", "Please enter a company name and API key.")
        logging.warning("Input Error: Company name or API key missing")

def generate_document():
    logging.info("Generating document")
    company_name = entry.get()
    api_key = api_entry.get()
    user_demand2 = document_demand_text.get("1.0", tk.END).strip()
    if company_name and api_key:
        try:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Generating document for {company_name}...\n")
            root.update()  # Update the GUI to show the message
            
            # Import the module
            import run_main_all
            
            # Run the main function
            result = run_main_all.main(company_name, api_key, user_demand2)
            
            # Display result
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, str(result))
            logging.info(f"Completed: {result}")
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, error_msg)
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)
    else:
        messagebox.showwarning("Input Error", "Please enter a company name and API key.")
        logging.warning("Input Error: Company name or API key missing")

def revise_document():
    logging.info("Revising document")
    company_name = entry.get()
    api_key = api_entry.get()
    revision_demand = revision_demand_text.get("1.0", tk.END).strip()
    if company_name and api_key:
        try:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Revising document for {company_name}...\n")
            root.update()  # Update the GUI to show the message
            
            # Step 1: Run revise_document.py to revise individual files
            logging.info("Starting document revision")
            import revise_document
            result_revise = revise_document.revise_document(company_name, api_key, revision_demand)
            
            # Step 2: Read sections and combine files (like in run_main_all.py)
            logging.info("Combining revised sections")
            with open("table_of_content.txt", "r", encoding="utf-8") as file:
                sections = [line.strip() for line in file if line.strip()]
            
            # Combine files into output.txt
            combined_content = []
            for i, section in enumerate(sections, 1):
                with open(f"{i}.txt", "r", encoding="utf-8") as file:
                    content = file.read()
                    combined_content.append(f"{section}\n\n{content}\n\n")
            
            with open("output.txt", "w", encoding="utf-8") as file:
                file.write("\n".join(combined_content))
            
            # Step 3: Convert to Word document
            logging.info("Converting to Word document")
            import main4
            result_main4 = main4.main(company_name, revision_demand)
            
            # Display results
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, 
                f"Document revision completed for {company_name}:\n"
                f"Initial revision: {result_revise}\n"
                f"Document conversion: {result_main4}")
            
            logging.info("Document revision process completed")
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, error_msg)
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)
    else:
        messagebox.showwarning("Input Error", "Please enter a company name and API key.")
        logging.warning("Input Error: Company name or API key missing")

# Create the main window
root = tk.Tk()
root.title("案例生成器")
root.geometry("800x800")  # Increased height

# Create a font object
default_font = font.Font(size=12)

# First row: Entry for company name
tk.Label(root, text="请输入企业名称:", font=default_font).grid(row=0, column=0, padx=10, pady=10)
entry = tk.Entry(root, width=40, font=default_font)  # Increased width
entry.grid(row=0, column=1, padx=10, pady=10)

# Second row: Entry for API key
tk.Label(root, text="请输入Deepseek API密钥:", font=default_font).grid(row=1, column=0, padx=10, pady=10)
api_entry = tk.Entry(root, width=40, font=default_font)  # Increased width
api_entry.grid(row=1, column=1, padx=10, pady=10)
api_entry.insert(0, "sk-271298e918124857b6c9c3a8faa75cd6")  # Pre-fill your API key

# Third row: Entry for user demand
tk.Label(root, text="目录需求（选填）:", font=default_font).grid(row=2, column=0, padx=10, pady=10, sticky="n")
demand_text = scrolledtext.ScrolledText(root, width=40, height=3, font=default_font)
demand_text.grid(row=2, column=1, padx=10, pady=10)

# Fourth row: New entry for document demand
tk.Label(root, text="生成文件要求（选填）:", font=default_font).grid(row=3, column=0, padx=10, pady=10, sticky="n")
document_demand_text = scrolledtext.ScrolledText(root, width=40, height=3, font=default_font)
document_demand_text.grid(row=3, column=1, padx=10, pady=10)

# Fifth row: New entry for revision demand
tk.Label(root, text="修改文件要求（选填）:", font=default_font).grid(row=4, column=0, padx=10, pady=10, sticky="n")
revision_demand_text = scrolledtext.ScrolledText(root, width=40, height=3, font=default_font)
revision_demand_text.grid(row=4, column=1, padx=10, pady=10)

# Sixth row: Description and button to generate table of content
tk.Label(root, text="生成目录", font=default_font).grid(row=5, column=0, padx=10, pady=10)
tk.Button(root, text="➤", bg="green", fg="white", command=generate_table_of_content, font=default_font).grid(row=5, column=1, padx=10, pady=10)

# Seventh row: Description and button to search the internet
tk.Label(root, text="网络爬取相关资讯", font=default_font).grid(row=6, column=0, padx=10, pady=10)
tk.Button(root, text="搜索", bg="green", fg="white", command=search_internet, font=default_font).grid(row=6, column=1, padx=5, pady=10, sticky="w")
tk.Button(root, text="处理结果", bg="blue", fg="white", command=process_search_results, font=default_font).grid(row=6, column=1, padx=5, pady=10, sticky="e")

# Eighth row: Description and button to generate document
tk.Label(root, text="生成文件", font=default_font).grid(row=7, column=0, padx=10, pady=10)
tk.Button(root, text="➤", bg="green", fg="white", command=generate_document, font=default_font).grid(row=7, column=1, padx=10, pady=10)

# Ninth row: Description and button to revise document
tk.Label(root, text="修改文件", font=default_font).grid(row=8, column=0, padx=10, pady=10)
tk.Button(root, text="➤", bg="orange", fg="white", command=revise_document, font=default_font).grid(row=8, column=1, padx=10, pady=10)

# Tenth row: Text widget to display output messages
output_text = tk.Text(root, wrap=tk.WORD, width=80, height=15, font=default_font)  # Increased width and height
output_text.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# Start the main loop
root.mainloop()
