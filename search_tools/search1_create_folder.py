import os

def create_folders_and_files():
    # Read the table_of_content.txt file
    with open("table_of_content.txt", "r", encoding="utf-8") as file:
        sections = [line.strip() for line in file if line.strip()]  # Skip blank lines

    print(f"Hello Current Working Directory: {os.getcwd()}")
    print(f"Hello  Sections to process: {sections}")

    # Create folders and save section titles as .txt files
    for i, section_title in enumerate(sections):
        folder_name = str(i + 1)
        folder_path = os.path.join(os.getcwd(), folder_name)
        print(f"Hello2 Constructed Folder Path: {folder_path}")

        os.makedirs(folder_path, exist_ok=True)  # Create the folder
        print(f"Hello2  Created folder: {folder_path}")

        # Save the section title as a .txt file in the corresponding folder
        title_path = os.path.join(folder_path, f"title{folder_name}.txt")
        print(f"Hello3 Constructed Title File Path: {title_path}")

        with open(title_path, "w", encoding="utf-8") as section_file:
            section_file.write(section_title)
            print(f"Hello3 Created file: {title_path}")

    print("Folders and files created successfully!")

def main(company_name, api_key):
    try:
        # Call the original function
        create_folders_and_files()
        return "Folder creation completed successfully"
    except Exception as e:
        return f"Error in folder creation: {str(e)}"