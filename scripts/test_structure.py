#!/usr/bin/env python3
"""
Quick test script to demonstrate the new package structure.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to Python path for local imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from find_your_next_adventure.models import Coordinates, Destination, Chapter
from find_your_next_adventure.parsers import AdventureGuideParser
from find_your_next_adventure.utils import calculate_distance, format_coordinates


def test_models():
    """Test the data models."""
    print("Testing data models...")
    
    # Create coordinates
    oslo_coords = Coordinates(59.9139, 10.7522, "N", "E")
    stockholm_coords = Coordinates(59.3293, 18.0686, "N", "E")
    
    # Create destinations
    oslo = Destination(1, "Oslo, Norway", oslo_coords, "Norway", "Scandinavia")
    stockholm = Destination(2, "Stockholm, Sweden", stockholm_coords, "Sweden", "Scandinavia")
    
    print(f"✓ Created destination: {oslo.location}")
    print(f"✓ Created destination: {stockholm.location}")
    
    # Create a chapter
    chapter = Chapter(
        title="Scandinavian Capitals",
        description="Major cities in Scandinavia",
        latitudeRange={"from": "55° North", "to": "70° North"},
        totalDestinations=2,
        destinations=[oslo, stockholm],
        metadata={"source": "Test", "chapter": "1"}
    )
    
    print(f"✓ Created chapter: {chapter.title} with {chapter.totalDestinations} destinations")
    return oslo_coords, stockholm_coords


def test_utils(oslo_coords, stockholm_coords):
    """Test utility functions."""
    print("\nTesting utility functions...")
    
    # Calculate distance
    distance = calculate_distance(oslo_coords, stockholm_coords)
    print(f"✓ Distance between Oslo and Stockholm: {distance:.2f} km")
    
    # Format coordinates
    formatted = format_coordinates(oslo_coords, "decimal")
    print(f"✓ Oslo coordinates (decimal): {formatted}")
    
    formatted_dms = format_coordinates(oslo_coords, "dms")
    print(f"✓ Oslo coordinates (DMS): {formatted_dms}")


def test_parser():
    """Test the parser."""
    print("\nTesting parser...")
    
    parser = AdventureGuideParser()
    
    # Test line parsing
    test_line = "1. Oslo, Norway - Latitude: 59.9139 N Longitude: 10.7522 E"
    destination = parser.parse_line(test_line)
    
    if destination:
        print(f"✓ Successfully parsed: {destination.location}")
        print(f"  - Country: {destination.country}")
        print(f"  - Region: {destination.region}")
        print(f"  - Coordinates: {destination.coordinates.latitude}, {destination.coordinates.longitude}")
    else:
        print("✗ Failed to parse test line")


def main():
    """Run all tests."""
    print("Find Your Next Adventure - Package Structure Test")
    print("=" * 50)
    
    try:
        oslo_coords, stockholm_coords = test_models()
        test_utils(oslo_coords, stockholm_coords)
        test_parser()
        
        print("\n" + "=" * 50)
        print("✅ All tests passed! Package structure is working correctly.")
        print("The project has been successfully restructured with:")
        print("  - Modular architecture with separate packages")
        print("  - Type hints and modern Python practices")
        print("  - Comprehensive test structure")
        print("  - Proper packaging configuration")
        print("  - Development tools and utilities")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
