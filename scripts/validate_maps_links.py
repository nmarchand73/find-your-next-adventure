#!/usr/bin/env python3
"""
Script to validate Google Maps links in the generated JSON files.
"""

import json
import urllib.parse
from pathlib import Path

def validate_google_maps_link(link: str, location: str) -> bool:
    """
    Validate that a Google Maps link is properly formatted.
    
    Args:
        link: The Google Maps link to validate
        location: The location name for context
    
    Returns:
        True if the link appears valid, False otherwise
    """
    if not link:
        print(f"❌ Empty link for: {location}")
        return False
    
    if not link.startswith("https://www.google.com/maps/search/"):
        print(f"❌ Invalid base URL for: {location}")
        return False
    
    try:
        # Extract the query part and decode it
        query_part = link.replace("https://www.google.com/maps/search/", "")
        if not query_part:
            print(f"❌ Empty query for: {location}")
            return False
        
        # URL decode the query
        decoded_query = urllib.parse.unquote(query_part)
        
        # Check if it contains coordinates pattern (@lat,lng)
        if "@" not in decoded_query or "," not in decoded_query:
            print(f"❌ Missing coordinates pattern for: {location}")
            return False
        
        # Extract coordinates part after @
        coords_part = decoded_query.split("@")[1] if "@" in decoded_query else ""
        if not coords_part:
            print(f"❌ No coordinates found after @ for: {location}")
            return False
            
        # Check if coordinates look valid (should have lat,lng format)
        coords_values = coords_part.split(",")[:2]  # Take first two values (lat,lng)
        if len(coords_values) < 2:
            print(f"❌ Invalid coordinates format for: {location}")
            return False
            
        try:
            lat = float(coords_values[0])
            lng = float(coords_values[1])
            if not (-90 <= lat <= 90 and -180 <= lng <= 180):
                print(f"❌ Coordinates out of range for: {location} ({lat}, {lng})")
                return False
        except ValueError:
            print(f"❌ Non-numeric coordinates for: {location}")
            return False
        
        print(f"✅ Valid link for: {location} ({lat}, {lng})")
        return True
        
    except Exception as e:
        print(f"❌ Error validating link for {location}: {e}")
        return False

def main():
    """Main function to validate Google Maps links in all JSON files."""
    output_dir = Path("output")
    
    if not output_dir.exists():
        print("❌ Output directory not found")
        return
    
    json_files = list(output_dir.glob("chapter_*.json"))
    if not json_files:
        print("❌ No chapter JSON files found")
        return
    
    total_destinations = 0
    valid_links = 0
    invalid_links = 0
    
    for json_file in sorted(json_files):
        print(f"\n📄 Checking {json_file.name}:")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            destinations = data.get('destinations', [])
            print(f"   Found {len(destinations)} destinations")
            
            for dest in destinations[:5]:  # Check first 5 in each file
                location = dest.get('location', 'Unknown')
                google_link = dest.get('googleMapsLink', '')
                
                total_destinations += 1
                if validate_google_maps_link(google_link, location):
                    valid_links += 1
                else:
                    invalid_links += 1
                    
        except Exception as e:
            print(f"❌ Error reading {json_file}: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   Total destinations checked: {total_destinations}")
    print(f"   Valid Google Maps links: {valid_links}")
    print(f"   Invalid links: {invalid_links}")
    print(f"   Success rate: {(valid_links/total_destinations)*100:.1f}%" if total_destinations > 0 else "N/A")
    
    # Show a few example links
    if valid_links > 0:
        print(f"\n🔗 Example working links:")
        for json_file in sorted(json_files)[:2]:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                dest = data.get('destinations', [])[0] if data.get('destinations') else None
                if dest:
                    print(f"   {dest['location']}: {dest['googleMapsLink']}")
            except:
                pass

if __name__ == "__main__":
    main()
