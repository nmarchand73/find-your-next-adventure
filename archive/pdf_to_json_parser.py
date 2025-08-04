#!/usr/bin/env python3
"""
JSON Generator for "Find Your Next Adventure" Guide
Extracts destinations from PDF and generates structured JSON files.
"""

import sys
import logging
from pathlib import Path
from find_your_next_adventure.parsers import AdventureGuideParser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    
    if len(sys.argv) != 3:
        print("Usage: python pdf_to_json_parser.py <pdf_file> <output_directory>")
        print("Example: python pdf_to_json_parser.py adventure_guide.pdf ./json_output/")
        sys.exit(1)
    
    pdf_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    
    if not pdf_path.exists():
        logger.error(f"PDF file not found: {pdf_path}")
        sys.exit(1)
    
    parser = AdventureGuideParser()
    parser.process_pdf(pdf_path, output_dir)

def test_parser():
    sample_content = """
    45. ST. PETERSBURG, RUSSIA - Latitude: 59.9342 N Longitude: 30.3350 E
    306. ISTANBUL, TURKEY - Latitude: 41.0082 N Longitude: 28.9783 E
    530. MARRAKECH, MOROCCO - Latitude: 31.6414 N Longitude: 8.0023 W
    787. THE MALDIVES - Latitude: 3.6164 N Longitude: 72.7164 E
    925. EASTER ISLAND, CHILE - Latitude: 27.1167 S Longitude: 109.3667 W
    """
    
    parser = AdventureGuideParser()
    chapters_data = parser.parse_pdf_content(sample_content)
    
    total = sum(len(destinations) for destinations in chapters_data.values())
    print(f"Test results: {total} destinations parsed successfully")
    
    for chapter_num, destinations in chapters_data.items():
        for dest in destinations[:2]:
            print(f"  {dest.id}: {dest.location} -> {dest.country}")

if __name__ == "__main__":


    if len(sys.argv) == 1:
        test_parser()
    else:
        main()