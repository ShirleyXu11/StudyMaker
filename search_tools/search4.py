import os
import shutil

def get_base_directory():
    base_dir = os.getcwd()
    print(f"Determined Base Directory: {base_dir}")
    return base_dir

def process_files():
    base_directory = get_base_directory()
    
    for i in range(1, 51):
        folder_name = str(i)
        folder_path = os.path.join(base_directory, folder_name)
        print(f"Constructed Folder Path: {folder_path}")
        
        # Ensure the folder exists in the base directory
        if not os.path.exists(folder_path):
            # print(f"Folder {folder_path} does not exist. Skipping.")
            continue

        output_file = os.path.join(folder_path, 'search_results.txt')
        print(f"Constructed Output File Path: {output_file}")

        # Clear the output file if it already exists
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
                print(f"Removed existing output file: {output_file}")
            except PermissionError as e:
                print(f'PermissionError: {e}. Skipping removal of {output_file}.')
                continue

        # Loop over j = 1, ..., 100 and k = 1, ..., 100
        for j in range(1, 101):
            for k in range(1, 101):
                file_name = f'search{j}_{k}.txt'
                temp_file_path = os.path.join(folder_path, file_name)
                exe_file_path = os.path.join(base_directory, folder_name, file_name)
                # print(f"Constructed Temp File Path: {temp_file_path}")
                # print(f"Constructed Exe File Path: {exe_file_path}")

                # Move the file from the temporary directory to the executable's directory
                # if os.path.exists(temp_file_path):
                #     try:
                #         shutil.move(temp_file_path, exe_file_path)
                #         print(f"Moved file {temp_file_path} to {exe_file_path}")
                #     except Exception as e:
                #         print(f"Error moving file {temp_file_path}: {str(e)}")
                #         continue

                if not os.path.exists(exe_file_path):
                    # print(f"File {exe_file_path} does not exist. Skipping.")
                    continue

                try:
                    # Try different encodings
                    encodings = ['utf-8', 'latin1', 'cp1252']
                    content = None

                    for encoding in encodings:
                        try:
                            with open(exe_file_path, 'r', encoding=encoding) as file:
                                content = file.read()
                                break
                        except UnicodeDecodeError:
                            continue

                    if content is not None:
                        with open(output_file, 'a', encoding='utf-8') as out_file:
                            out_file.write(content)
                            out_file.write('\n\n')

                except Exception as e:
                    print(f'Error processing file {exe_file_path}: {str(e)}')

        print(f'All contents from folder {folder_name} have been saved to {output_file}')

def main(company_name, api_key):
    try:
        # Call the original process_files function
        process_files()
        return "Search4 completed successfully"
    except Exception as e:
        return f"Error in search4: {str(e)}"

if __name__ == "__main__":
    process_files()