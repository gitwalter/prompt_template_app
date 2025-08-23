"""
Script to import CSV data into the prompt_templates database.

This script reads the development_prompts.csv file and imports the data
into the prompt_templates table in the SQLite database.
"""

import csv
import sys
from prompt_template_database import session, PromptTemplate

def import_csv_to_database(csv_file_path):
    """
    Import CSV data into the prompt_templates database.
    
    Args:
        csv_file_path (str): Path to the CSV file to import
    """
    try:
        # Read CSV file with pipe delimiter
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='|')
            
            imported_count = 0
            skipped_count = 0
            
            for row in reader:
                # Check if template already exists
                existing_template = PromptTemplate.get_by_name(session, row['name'])
                
                if existing_template:
                    print(f"Skipping '{row['name']}' - already exists in database")
                    skipped_count += 1
                    continue
                
                # Create new template with default use_web_search=False
                new_template = PromptTemplate(
                    topic=row['topic'],
                    name=row['name'],
                    purpose=row['purpose'],
                    template=row['template'],
                    use_web_search=False  # Default value
                )
                
                session.add(new_template)
                imported_count += 1
                print(f"Imported: {row['name']}")
            
            # Commit all changes
            session.commit()
            
            print(f"\nImport completed!")
            print(f"Imported: {imported_count} templates")
            print(f"Skipped: {skipped_count} templates (already existed)")
            
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during import: {e}")
        session.rollback()
        sys.exit(1)

def main():
    """Main function to run the import."""
    csv_file = "development_prompts.csv"
    
    print(f"Starting import from {csv_file}...")
    print("=" * 50)
    
    import_csv_to_database(csv_file)
    
    print("=" * 50)
    print("Import process finished.")

if __name__ == "__main__":
    main()
