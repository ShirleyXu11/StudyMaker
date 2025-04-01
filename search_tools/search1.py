import os
import glob

def split_file_by_characters(file_path, chunk_size=300, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        content = file.read()
    
    characters = list(content)
    chunks = [characters[i:i + chunk_size] for i in range(0, len(characters), chunk_size)]
    
    base_name = os.path.basename(file_path)
    file_name, file_ext = os.path.splitext(base_name)
    
    for i, chunk in enumerate(chunks):
        chunk_file_name = f"{file_name}_{i+1}{file_ext}"
        with open(chunk_file_name, 'w', encoding=encoding) as chunk_file:
            chunk_file.write(''.join(chunk))

def process_files(file_pattern, encoding='utf-8'):
    file_list = glob.glob(file_pattern)
    for file_path in file_list:
        split_file_by_characters(file_path, encoding=encoding)
        # Remove the original file after splitting
        os.remove(file_path)

def main(company_name, api_key):
    try:
        # Pattern to match all files like search1.txt, search2.txt, etc.
        file_pattern = 'search*.txt'
        # Process each file using the original function
        process_files(file_pattern)
        return "Search1 completed successfully"
    except Exception as e:
        return f"Error in search1: {str(e)}"