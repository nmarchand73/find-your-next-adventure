# Find Your Next Adventure

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A simple Python tool to extract adventure destinations from PDF travel guides and convert them to structured JSON format.

## 🚀 Quick Start

### Simple Usage
```bash
# Parse your own PDF
python run.py "my_adventure_guide.pdf" "./output/"

# Run with sample PDF (no arguments)
python run.py
```

### Programmatic Usage
```python
from find_your_next_adventure.parsers.adventure_guide_parser import AdventureGuideParser

# Initialize parser
parser = AdventureGuideParser()

# Parse PDF and generate JSON files
parser.process_pdf("adventure_guide.pdf", "./output/")

# Get statistics
stats = parser.get_stats()
print(f"Parsed {stats['successful']} destinations successfully!")
```

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/nmarchand73/find-your-next-adventure.git
cd find-your-next-adventure

# Install the package
pip install -e .

# For development
pip install -e ".[dev]"
```

## 🎯 Features

- **PDF Parsing**: Extract destinations from travel guide PDFs
- **Geographic Organization**: Auto-organize by latitude regions
- **Coordinate Processing**: Parse and validate GPS coordinates
- **AI-Powered Attractions**: Generate main attractions in English and French using Ollama with phi4-mini model
- **JSON Output**: Generate structured JSON files by region
- **Generation Logging**: Detailed logs of all AI generation calls for debugging and analysis
- **Simple Interface**: Easy-to-use command line tool

## 📁 Project Structure

```
find-your-next-adventure/
├── run.py                           # Single command-line interface
├── find_your_next_adventure/        # Main package
│   ├── models/                      # Data models
│   ├── parsers/                     # PDF parsing logic
│   └── utils/                       # Utilities
├── tests/                           # Test suite
├── output/                          # Generated JSON files
└── FindYourNextAdventure.pdf        # Sample PDF
```

## 📝 Logging

The application uses centralized logging to track all operations. All logs are written to a single file:

- **Log File**: `logs/find_your_next_adventure.log`
- **Log Level**: INFO (configurable)
- **Rotation**: Automatic rotation when file reaches 10MB
- **Backup**: Keeps 5 backup files

### Log Contents

The log file contains:
- Session start/end information
- PDF processing progress
- AI generation calls and responses
- Error messages and fallbacks
- Performance statistics

### Example Log Entry

```
2025-08-04 23:40:37 - find_your_next_adventure.utils.logging_config - INFO - SESSION STARTED
2025-08-04 23:40:37 - find_your_next_adventure.parsers.adventure_guide_parser - INFO - Processing: FindYourNextAdventure.pdf
2025-08-04 23:41:19 - find_your_next_adventure.utils.ollama_generator - INFO - [23:41:19] BATCH: 5 locations processed in single prompt
```

## 🌍 Output Format

The tool generates JSON files organized by latitude ranges:

- `chapter_1_destinations.json` - Arctic (90°N to 60°N)
- `chapter_2_destinations.json` - Northern (60°N to 45°N)
- `chapter_3_destinations.json` - Mid-northern (45°N to 30°N)
- `chapter_4_destinations.json` - Northern tropics (30°N to 15°N)
- `chapter_5_destinations.json` - Equatorial north (15°N to 0°)
- `chapter_6_destinations.json` - Equatorial south (0° to 15°S)
- `chapter_7_destinations.json` - Southern (15°S to 30°S)
- `chapter_8_destinations.json` - Antarctic (30°S to 90°S)
- `complete_adventure_guide.json` - Combined dataset

### Example JSON Structure

```json
{
  "title": "Find Your Next Adventure - Chapter 1: From 90° North to 60° North",
  "description": "Adventure destinations from 90° north to 60° north",
  "latitudeRange": {"from": "90° North", "to": "60° North"},
  "totalDestinations": 44,
  "destinations": [
    {
      "id": 1,
      "location": "Svalbard, Norway",
      "coordinates": {
        "latitude": 78.2208,
        "longitude": 15.6401,
        "latitudeDirection": "N",
        "longitudeDirection": "E"
      },
      "country": "Norway",
      "region": "Scandinavia",
      "mainAttractionEn": "Experience the raw beauty of Arctic wilderness with polar bear encounters and stunning glaciers.",
      "mainAttractionFr": "Découvrez la beauté sauvage de l'Arctique avec des rencontres d'ours polaires et des glaciers époustouflants.",
      "googleMapsLink": "https://maps.google.com/?q=78.2208,15.6401"
    }
  ]
}
```

## 🛠️ Development

```bash
# Run tests
pytest

# Format code
black find_your_next_adventure tests

# Lint code
flake8 find_your_next_adventure tests

# Type checking
mypy find_your_next_adventure
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

**Made with ❤️ for adventure seekers everywhere!**
