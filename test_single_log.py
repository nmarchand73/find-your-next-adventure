#!/usr/bin/env python3
"""
Test script for single log file approach.
"""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from find_your_next_adventure.utils.ollama_generator import OllamaGenerator

def test_single_log():
    """Test single log file approach."""
    print("🧪 Testing single log file approach...")
    print("=" * 60)
    
    # Create first generator
    print("📦 Creating first generator...")
    generator1 = OllamaGenerator(batch_size=2)
    
    # Test locations
    test_locations = [
        {"location": "Paris", "country": "France", "region": "Western Europe"},
        {"location": "Tokyo", "country": "Japan", "region": "East Asia"}
    ]
    
    print(f"📋 Adding {len(test_locations)} locations...")
    for loc in test_locations:
        en_result, fr_result = generator1.generate_attractions(
            loc['location'], loc['country'], loc['region']
        )
        print(f"   📍 Added: {loc['location']}")
    
    # Process batch
    print("\n🔄 Processing batch...")
    generator1.process_batch(force=True)
    
    print(f"\n📝 First log file: {generator1.log_file}")
    
    # Create second generator (should use same log file)
    print("\n📦 Creating second generator...")
    generator2 = OllamaGenerator(batch_size=2)
    
    print(f"📋 Adding {len(test_locations)} locations...")
    for loc in test_locations:
        en_result, fr_result = generator2.generate_attractions(
            loc['location'], loc['country'], loc['region']
        )
        print(f"   📍 Added: {loc['location']}")
    
    # Process batch
    print("\n🔄 Processing batch...")
    generator2.process_batch(force=True)
    
    print(f"\n📝 Second log file: {generator2.log_file}")
    
    # Check if files are the same
    if generator1.log_file == generator2.log_file:
        print("✅ Same log file used for both generators!")
    else:
        print("❌ Different log files created!")
    
    # Show log file content
    print(f"\n📄 Log file content preview:")
    try:
        with open(generator1.log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"   Total lines: {len(lines)}")
            print(f"   First 3 lines:")
            for i, line in enumerate(lines[:3], 1):
                print(f"   {i}. {line.strip()}")
            if len(lines) > 3:
                print(f"   ... and {len(lines) - 3} more lines")
    except FileNotFoundError:
        print("   ❌ Log file not found")
    
    print("\n✅ Single log file test completed!")

if __name__ == "__main__":
    test_single_log() 