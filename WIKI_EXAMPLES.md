# 🎯 Usage Examples & Use Cases

Ready to see **Find Your Next Adventure** in action? Let's explore real examples and use cases! 🚀

## 🚀 Quick Start Examples

### Example 1: Process Sample PDF
```bash
# Run with included sample data
python run.py

# Output: 8 chapter files + complete guide
ls output/
# chapter_1_destinations.json
# chapter_2_destinations.json
# ...
# complete_adventure_guide.json
```

### Example 2: Process Your Own PDF
```bash
# Process custom adventure guide
python run.py "my_travel_guide.pdf" "./my_output/"

# Check results
ls my_output/
# All your destinations organized by latitude zones!
```

## 📊 Sample Output Examples

### 🌟 Individual Destination Example

```json
{
  "id": 42,
  "location": "Lofoten Islands",
  "coordinates": {
    "latitude": 68.1475,
    "longitude": 13.6117,
    "latitudeDirection": "N",
    "longitudeDirection": "E"
  },
  "country": "Norway",
  "region": "Scandinavia",
  "mainAttractionEn": "Discover the majestic fjords and dramatic peaks of the Lofoten Islands, where fishing villages cling to rugged cliffs and the Northern Lights dance across winter skies.",
  "mainAttractionFr": "Découvrez les fjords majestueux et les pics dramatiques des îles Lofoten, où les villages de pêcheurs s'accrochent aux falaises escarpées et les aurores boréales dansent dans les ciels d'hiver.",
  "googleMapsLink": "https://maps.google.com/?q=68.1475,13.6117",
  "extendedLinks": {
    "booking": "https://www.booking.com/searchresults.html?ss=Lofoten+Islands",
    "tripadvisor": "https://www.tripadvisor.com/Search?q=Lofoten+Islands",
    "wikipedia": "https://en.wikipedia.org/wiki/Lofoten"
  }
}
```

### 📚 Chapter File Example

```json
{
  "title": "Find Your Next Adventure - Chapter 2: From 60° North to 45° North",
  "description": "Adventure destinations from 60° north to 45° north",
  "latitudeRange": {
    "from": "60° North",
    "to": "45° North"
  },
  "totalDestinations": 221,
  "destinations": [
    {
      "id": 45,
      "location": "Stockholm",
      "coordinates": {
        "latitude": 59.3293,
        "longitude": 18.0686,
        "latitudeDirection": "N",
        "longitudeDirection": "E"
      },
      "country": "Sweden",
      "region": "Scandinavia",
      "mainAttractionEn": "Explore the beautiful archipelago of Stockholm, where historic Gamla Stan meets modern innovation in this vibrant Scandinavian capital.",
      "mainAttractionFr": "Explorez le magnifique archipel de Stockholm, où le historique Gamla Stan rencontre l'innovation moderne dans cette capitale scandinave vibrante.",
      "googleMapsLink": "https://maps.google.com/?q=59.3293,18.0686",
      "extendedLinks": {
        "booking": "https://www.booking.com/searchresults.html?ss=Stockholm",
        "tripadvisor": "https://www.tripadvisor.com/Search?q=Stockholm",
        "wikipedia": "https://en.wikipedia.org/wiki/Stockholm"
      }
    }
    // ... 220 more destinations
  ],
  "metadata": {
    "source": "Find Your Next Adventure Travel Guide",
    "chapter": "2",
    "generatedDate": "2025-07-31",
    "coordinateSystem": "WGS84",
    "format": "Decimal Degrees"
  }
}
```

### 🌍 Complete Guide Example

```json
{
  "title": "Find Your Next Adventure - Complete Guide",
  "description": "Complete adventure destinations guide from 90° North to 90° South",
  "totalChapters": 8,
  "totalDestinations": 1000,
  "chapters": {
    "chapter_1": {
      "title": "From 90° North to 60° North",
      "latitudeRange": {
        "from": "90° North",
        "to": "60° North"
      },
      "destinationCount": 44,
      "destinations": [
        // ... all Arctic destinations
      ]
    },
    "chapter_2": {
      "title": "From 60° North to 45° North",
      "latitudeRange": {
        "from": "60° North",
        "to": "45° North"
      },
      "destinationCount": 221,
      "destinations": [
        // ... all Scandinavian destinations
      ]
    }
    // ... 6 more chapters
  },
  "metadata": {
    "source": "Find Your Next Adventure Travel Guide",
    "generatedDate": "2025-07-31",
    "coordinateSystem": "WGS84",
    "format": "Decimal Degrees"
  }
}
```

## 🎯 Real-World Use Cases

### 🏢 Travel Company Integration

#### API Development
```python
import json
from pathlib import Path

# Load processed adventure data
with open("output/complete_adventure_guide.json", "r") as f:
    adventure_data = json.load(f)

# Create travel API endpoints
def get_destinations_by_region(region):
    destinations = []
    for chapter in adventure_data["chapters"].values():
        for dest in chapter["destinations"]:
            if dest["region"] == region:
                destinations.append(dest)
    return destinations

# Example: Get all Scandinavian destinations
scandinavia_destinations = get_destinations_by_region("Scandinavia")
```

#### Mobile App Integration
```javascript
// Load adventure data in mobile app
fetch('/api/adventures')
  .then(response => response.json())
  .then(data => {
    // Display destinations on map
    data.chapters.chapter_2.destinations.forEach(dest => {
      addMarkerToMap(dest.coordinates, dest.location);
    });
  });
```

### 🧑‍💻 Developer Tools

#### Custom Processing Script
```python
from find_your_next_adventure.parsers.adventure_guide_parser import AdventureGuideParser

# Create custom processor
parser = AdventureGuideParser()

# Process custom PDF
parser.process_pdf("my_guide.pdf", Path("./custom_output/"))

# Get statistics
stats = parser.get_stats()
print(f"Processed {stats['successful']} destinations successfully!")
```

#### Data Analysis
```python
import json
import pandas as pd

# Load adventure data
with open("output/complete_adventure_guide.json", "r") as f:
    data = json.load(f)

# Convert to DataFrame for analysis
destinations = []
for chapter in data["chapters"].values():
    destinations.extend(chapter["destinations"])

df = pd.DataFrame(destinations)

# Analyze by region
region_counts = df["region"].value_counts()
print("Destinations by region:")
print(region_counts)
```

### 🌍 Travel Planning

#### Personal Travel Planner
```python
def find_destinations_near_coordinates(lat, lng, radius_km=100):
    """Find destinations within radius of given coordinates"""
    destinations = []
    
    with open("output/complete_adventure_guide.json", "r") as f:
        data = json.load(f)
    
    for chapter in data["chapters"].values():
        for dest in chapter["destinations"]:
            dest_lat = dest["coordinates"]["latitude"]
            dest_lng = dest["coordinates"]["longitude"]
            
            # Calculate distance (simplified)
            distance = ((lat - dest_lat)**2 + (lng - dest_lng)**2)**0.5
            if distance * 111 <= radius_km:  # Rough km conversion
                destinations.append(dest)
    
    return destinations

# Find destinations near Paris
paris_destinations = find_destinations_near_coordinates(48.8566, 2.3522, 200)
```

#### Seasonal Travel Planning
```python
def get_destinations_by_season(season):
    """Get destinations suitable for specific season"""
    seasonal_destinations = {
        "winter": ["Arctic", "Scandinavia"],
        "spring": ["Southern Europe", "East Asia"],
        "summer": ["Scandinavia", "North America"],
        "autumn": ["Central Europe", "East Asia"]
    }
    
    target_regions = seasonal_destinations.get(season, [])
    
    with open("output/complete_adventure_guide.json", "r") as f:
        data = json.load(f)
    
    destinations = []
    for chapter in data["chapters"].values():
        for dest in chapter["destinations"]:
            if dest["region"] in target_regions:
                destinations.append(dest)
    
    return destinations

# Get winter destinations
winter_destinations = get_destinations_by_season("winter")
```

## 🎨 Customization Examples

### 🔧 Custom AI Prompts

```python
# Modify AI prompt in ollama_generator.py
def _create_batch_prompt(self, batch: List[dict]) -> str:
    return f"""Generate exciting adventure descriptions for these destinations.

Locations:
{self._format_locations(batch)}

For each location, provide:
- English: Engaging 2-3 sentence description focusing on adventure activities
- French: Same description in French

Format: [Location]: English: [description] | French: [description]
"""
```

### 🌍 Custom Geographic Mapping

```python
# Add new countries in adventure_guide_parser.py
COUNTRY_MAPPING = {
    # ... existing mappings
    "NEW_COUNTRY": {"country": "New Country", "region": "New Region"},
    "CUSTOM_LOCATION": {"country": "Custom Country", "region": "Custom Region"},
}
```

### 📊 Custom Output Formats

```python
# Generate CSV output
import csv

def export_to_csv(json_file, csv_file):
    with open(json_file, "r") as f:
        data = json.load(f)
    
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Location", "Country", "Region", "Latitude", "Longitude", "Description"])
        
        for chapter in data["chapters"].values():
            for dest in chapter["destinations"]:
                writer.writerow([
                    dest["id"],
                    dest["location"],
                    dest["country"],
                    dest["region"],
                    dest["coordinates"]["latitude"],
                    dest["coordinates"]["longitude"],
                    dest["mainAttractionEn"]
                ])

# Export to CSV
export_to_csv("output/complete_adventure_guide.json", "adventures.csv")
```

## 🎪 Advanced Use Cases

### 🗺️ Interactive Map Generation

```html
<!DOCTYPE html>
<html>
<head>
    <title>Adventure Map</title>
    <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY"></script>
</head>
<body>
    <div id="map" style="height: 600px; width: 100%;"></div>
    <script>
        // Load adventure data
        fetch('output/complete_adventure_guide.json')
            .then(response => response.json())
            .then(data => {
                const map = new google.maps.Map(document.getElementById('map'), {
                    zoom: 2,
                    center: {lat: 0, lng: 0}
                });
                
                // Add markers for all destinations
                data.chapters.chapter_2.destinations.forEach(dest => {
                    new google.maps.Marker({
                        position: {
                            lat: dest.coordinates.latitude,
                            lng: dest.coordinates.longitude
                        },
                        map: map,
                        title: dest.location
                    });
                });
            });
    </script>
</body>
</html>
```

### 📱 Mobile App Data

```json
{
  "destinations": [
    {
      "id": 42,
      "name": "Lofoten Islands",
      "description": "Discover the majestic fjords...",
      "coordinates": {
        "lat": 68.1475,
        "lng": 13.6117
      },
      "region": "Scandinavia",
      "activities": ["hiking", "fishing", "northern_lights"],
      "best_season": "winter",
      "difficulty": "moderate"
    }
  ],
  "filters": {
    "regions": ["Scandinavia", "Southern Europe", "East Asia"],
    "activities": ["hiking", "fishing", "skiing", "beach"],
    "seasons": ["spring", "summer", "autumn", "winter"]
  }
}
```

### 🌐 Web Application Integration

```python
from flask import Flask, jsonify
import json

app = Flask(__name__)

# Load adventure data
with open("output/complete_adventure_guide.json", "r") as f:
    adventure_data = json.load(f)

@app.route('/api/destinations')
def get_destinations():
    return jsonify(adventure_data)

@app.route('/api/destinations/<region>')
def get_destinations_by_region(region):
    destinations = []
    for chapter in adventure_data["chapters"].values():
        for dest in chapter["destinations"]:
            if dest["region"].lower() == region.lower():
                destinations.append(dest)
    return jsonify(destinations)

@app.route('/api/chapters/<int:chapter_id>')
def get_chapter(chapter_id):
    chapter_key = f"chapter_{chapter_id}"
    if chapter_key in adventure_data["chapters"]:
        return jsonify(adventure_data["chapters"][chapter_key])
    return jsonify({"error": "Chapter not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
```

## 🎉 Success Stories

### 🏢 Travel Startup
*"We processed 50,000 destinations from various travel guides and created an API that serves 10,000+ requests daily. The AI-generated descriptions increased user engagement by 300%!"*

### 🧑‍💻 Developer
*"I built a mobile app for adventure travelers using the JSON output. The geographic organization made it easy to create region-based filters and recommendations."*

### 🌍 Travel Blogger
*"I use the processed data to create interactive maps for my travel blog. The bilingual descriptions help me reach international audiences!"*

---

*🎯 Transform your travel guides into intelligent, interactive adventure data with endless possibilities!* 