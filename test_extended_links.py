#!/usr/bin/env python3
"""Test script for extended links functionality."""

from find_your_next_adventure.parsers.adventure_guide_parser import AdventureGuideParser
from find_your_next_adventure.models.coordinates import Coordinates
import json
from dataclasses import asdict

def test_extended_links():
    """Test the new extended links functionality."""
    parser = AdventureGuideParser()
    test_line = '9. JOSTEDAL, NORWAY - Latitude: 61.7106 N Longitude: 6.9241 E'
    
    print(f"Testing line: {test_line}")
    result = parser.parse_line(test_line)
    
    if result:
        print("✅ Successfully parsed the test line!")
        print("\nGenerated JSON structure:")
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    else:
        print("❌ Failed to parse test line")
        print(f"Failed lines: {parser.failed_lines}")

if __name__ == "__main__":
    test_extended_links()
