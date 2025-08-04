#!/usr/bin/env python3
"""
Main script to parse the PDF adventure guide and generate JSON files.
"""

import sys
from pathlib import Path
from find_your_next_adventure.parsers.adventure_guide_parser import AdventureGuideParser

def main():
    """Main function to run the PDF parser."""
    
    # Define paths
    workspace_root = Path(__file__).parent
    pdf_path = workspace_root / "FindYourNextAdventure.pdf"
    output_dir = workspace_root / "output"
    
    # Check if PDF exists
    if not pdf_path.exists():
        print(f"Error: PDF file not found at {pdf_path}")
        print("Please ensure 'FindYourNextAdventure.pdf' is in the project root.")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Initialize parser
    parser = AdventureGuideParser()
    
    print(f"Parsing PDF: {pdf_path}")
    print(f"Output directory: {output_dir}")
    
    try:
        # Parse the PDF and generate JSON files
        parser.process_pdf(pdf_path, output_dir)
        print("\n✅ PDF parsing completed successfully!")
        
        # Display statistics
        stats = parser.get_stats()
        print(f"\nStatistics:")
        print(f"  Successful destinations: {stats['successful']}")
        print(f"  Failed parsing attempts: {stats['failed']}")
        print(f"  Unknown countries: {stats['unknown_countries']}")
        
        # List generated files
        json_files = list(output_dir.glob("*.json"))
        if json_files:
            print(f"\nGenerated files:")
            for file in sorted(json_files):
                print(f"  - {file.name}")
        
    except Exception as e:
        print(f"❌ Error during parsing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
