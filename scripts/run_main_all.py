import logging
import sys
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def combine_section_files(sections):
    """Combine all section files into one"""
    combined_content = []
    for i, section in enumerate(sections, 1):
        try:
            with open(f"{i}.txt", "r", encoding="utf-8") as file:
                content = file.read()
                combined_content.append(f"{section}\n\n{content}\n\n")
        except Exception as e:
            logging.error(f"Error reading section {i}: {e}")
            raise
    
    # Save combined content to output.txt
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(combined_content))
    logging.info("Successfully combined all sections into output.txt")

def main(company_name, api_key, user_demand):
    try:
        logging.info(f"Starting document generation for company: {company_name}")
        
        # Check if table_of_content.txt exists
        if not os.path.exists("table_of_content.txt"):
            raise Exception("Please generate table of contents first")
        
        # Read sections from table of contents
        with open("table_of_content.txt", "r", encoding="utf-8") as file:
            sections = [line.strip() for line in file if line.strip()]
        
        if not sections:
            raise Exception("No sections found in table of contents")
        
        # Step 1: Run main2.py to generate individual section files
        logging.info("Starting main2.py - Initial document generation")
        import main2
        result_main2 = main2.main(company_name, api_key, user_demand)
        logging.info(f"main2.py completed: {result_main2}")
        
        # Combine section files into output.txt
        logging.info("Combining section files")
        combine_section_files(sections)
        
        # Step 2: Run main3.py for first revision
        logging.info("Starting main3.py - First revision")
        import main3
        result_main3 = main3.main(company_name, user_demand)
        logging.info(f"main3.py completed: {result_main3}")
        
        # Step 3: Run main4.py to convert to docx
        logging.info("Starting main4.py - Converting to Word document")
        import main4
        result_main4 = main4.main(company_name, user_demand)
        logging.info(f"main4.py completed: {result_main4}")
        
        return (f"Successfully generated case study for {company_name}.\n"
                f"Initial generation: {result_main2}\n"
                f"First revision: {result_main3}\n"
                f"Final conversion: {result_main4}")
        
    except Exception as e:
        error_msg = f"Error in document generation: {str(e)}"
        logging.error(error_msg)
        return error_msg

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python run_main_all.py <company_name> <api_key> [user_demand]")
        sys.exit(1)
        
    company_name = sys.argv[1]
    api_key = sys.argv[2]
    user_demand = sys.argv[3] if len(sys.argv) > 3 else ""
    
    result = main(company_name, api_key, user_demand)
    print(result)