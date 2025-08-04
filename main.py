#!/usr/bin/env python3
"""
Find Your Next Adventure - Simple PDF to JSON Parser
====================================================

A simple tool to extract adventure destinations from PDF files and convert them to JSON format.

Usage:
    python main.py [pdf_file] [output_directory]

Examples:
    python main.py "FindYourNextAdventure.pdf" "./output/"
    python main.py "my_adventure_guide.pdf" "/tmp/results/"
"""

import sys
import json
from pathlib import Path
from find_your_next_adventure.parsers.adventure_guide_parser import AdventureGuideParser

def main():
    """Simple main function for parsing PDF adventure guides."""
    
    # Get command line arguments
    if len(sys.argv) != 3:
        print(__doc__)
        print("\nError: Please provide PDF file and output directory.")
        print("Example: python main.py 'adventure.pdf' './output/'")
        sys.exit(1)
    
    pdf_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    
    # Validate inputs
    if not pdf_file.exists():
        print(f"❌ Error: PDF file not found: {pdf_file}")
        sys.exit(1)
    
    if not pdf_file.suffix.lower() == '.pdf':
        print(f"❌ Error: File must be a PDF: {pdf_file}")
        sys.exit(1)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("🚀 Find Your Next Adventure - PDF Parser")
    print("=" * 50)
    print(f"📄 PDF file: {pdf_file}")
    print(f"📁 Output directory: {output_dir}")
    print()
    
    try:
        # Initialize parser
        parser = AdventureGuideParser()
        
        # Parse the PDF
        print("🔄 Parsing PDF...")
        parser.process_pdf(pdf_file, output_dir)
        
        # Get statistics
        stats = parser.get_stats()
        
        print("\n✅ Parsing completed successfully!")
        print("=" * 50)
        print(f"📊 Statistics:")
        print(f"   • Successful destinations: {stats['successful']}")
        print(f"   • Failed parsing attempts: {stats['failed']}")
        print(f"   • Unknown countries: {stats['unknown_countries']}")
        
        # List generated files
        json_files = list(output_dir.glob("*.json"))
        if json_files:
            print(f"\n📁 Generated files:")
            for file in sorted(json_files):
                print(f"   • {file.name}")
        
        print(f"\n🎉 All done! Check the '{output_dir}' directory for your JSON files.")
        
    except Exception as e:
        print(f"❌ Error during parsing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 