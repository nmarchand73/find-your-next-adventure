#!/usr/bin/env python3
"""
Example: How to use Find Your Next Adventure parser
==================================================

This example shows how to use the parser in your own Python code.
"""

from pathlib import Path
from find_your_next_adventure.parsers.adventure_guide_parser import AdventureGuideParser

def example_usage():
    """Example of how to use the adventure guide parser."""
    
    # Initialize the parser
    parser = AdventureGuideParser()
    
    # Define your PDF file and output directory
    pdf_file = Path("FindYourNextAdventure.pdf")
    output_dir = Path("output")
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    print("🔍 Example: Parsing adventure guide...")
    
    # Parse the PDF
    parser.process_pdf(pdf_file, output_dir)
    
    # Get statistics
    stats = parser.get_stats()
    print(f"✅ Parsed {stats['successful']} destinations successfully!")
    
    # List generated files
    json_files = list(output_dir.glob("*.json"))
    print(f"📁 Generated {len(json_files)} JSON files:")
    for file in json_files:
        print(f"   • {file.name}")

if __name__ == "__main__":
    example_usage() 