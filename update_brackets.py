"""
Script to replace [] brackets with {} brackets in the database and CSV file.

This script updates the recently imported development templates to use {}
brackets instead of [] brackets for variable placeholders.
"""

import csv
import sys
from prompt_template_database import session, PromptTemplate

def update_database_brackets():
    """
    Update brackets in the database for recently imported templates.
    """
    # Get recently imported templates (the 8 new topics)
    recent_topics = [
        'Project Initialization and Planning',
        'Design and Architecture', 
        'Code Generation and Refinement',
        'Database Design and Query Optimization',
        'Documentation',
        'Testing, Debugging, and QA',
        'Security and Optimization',
        'Version Control and Collaboration'
    ]
    
    updated_count = 0
    
    for topic in recent_topics:
        templates = PromptTemplate.get_templates_by_topic(session, topic)
        
        for template in templates:
            # Check if template contains [] brackets
            if '[' in template.template and ']' in template.template:
                # Replace [] with {}
                old_template = template.template
                new_template = template.template.replace('[', '{').replace(']', '}')
                
                if old_template != new_template:
                    template.template = new_template
                    updated_count += 1
                    print(f"Updated: {template.name}")
    
    # Commit changes
    session.commit()
    print(f"\nDatabase update completed: {updated_count} templates updated")
    return updated_count

def update_csv_brackets():
    """
    Update brackets in the original CSV file.
    """
    csv_file = "development_prompts.csv"
    temp_file = "development_prompts_temp.csv"
    
    try:
        updated_count = 0
        
        # Read original file and write updated content to temp file
        with open(csv_file, 'r', encoding='utf-8') as infile, \
             open(temp_file, 'w', encoding='utf-8', newline='') as outfile:
            
            reader = csv.DictReader(infile, delimiter='|')
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames, delimiter='|')
            
            # Write header
            writer.writeheader()
            
            # Process each row
            for row in reader:
                # Check if template contains [] brackets
                if '[' in row['template'] and ']' in row['template']:
                    # Replace [] with {}
                    old_template = row['template']
                    new_template = row['template'].replace('[', '{').replace(']', '}')
                    
                    if old_template != new_template:
                        row['template'] = new_template
                        updated_count += 1
                        print(f"CSV Updated: {row['name']}")
                
                # Write the row (updated or unchanged)
                writer.writerow(row)
        
        # Replace original file with updated file
        import os
        os.replace(temp_file, csv_file)
        
        print(f"\nCSV update completed: {updated_count} templates updated")
        return updated_count
        
    except Exception as e:
        print(f"Error updating CSV: {e}")
        # Clean up temp file if it exists
        import os
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return 0

def main():
    """Main function to update brackets in both database and CSV."""
    print("Starting bracket replacement: [] -> {}")
    print("=" * 50)
    
    # Update database
    print("Updating database...")
    db_updated = update_database_brackets()
    
    print("\n" + "=" * 50)
    
    # Update CSV file
    print("Updating CSV file...")
    csv_updated = update_csv_brackets()
    
    print("\n" + "=" * 50)
    print("Bracket replacement completed!")
    print(f"Database templates updated: {db_updated}")
    print(f"CSV templates updated: {csv_updated}")

if __name__ == "__main__":
    main()
