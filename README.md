# Find Your Next Adventure

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Project Status: Active](https://img.shields.io/badge/Project%20Status-Active-brightgreen.svg)](https://github.com/nicolas-marchand/find-your-next-adventure)

A modern Python package for extracting structured JSON data from adventure travel guide PDFs. Parses destinations with coordinates and organizes them by geographic regions.

**✅ Status**: Complete with state-of-the-art Python architecture

## 🚀 Features

- **PDF Parsing**: Extract destinations from travel guide PDFs using PyMuPDF
- **Geographic Organization**: Auto-organize by regions/countries with comprehensive mapping
- **Coordinate Processing**: Parse, validate, and calculate distances between coordinates
- **Multi-format Output**: Individual chapter files + combined datasets
- **Modern Architecture**: Type-safe, modular design with CLI interface and utilities
- **Professional Tooling**: Full testing, linting, formatting, and development automation

## 📦 Installation

```bash
# Install from source (recommended)
git clone https://github.com/nicolas-marchand/find-your-next-adventure.git
cd find-your-next-adventure
pip install -e .

# Development installation
pip install -e ".[dev]"
# or
make install-dev
```

## 🎯 Quick Start

```bash
# Basic usage
python pdf_to_json_parser.py "guide.pdf" "./output/"

# Modern CLI with verbose output
python -m find_your_next_adventure.cli --verbose "guide.pdf" "./output/"

# Programmatic usage
from find_your_next_adventure.parsers import AdventureGuideParser
from find_your_next_adventure.models import Coordinates
from find_your_next_adventure.utils import calculate_distance

parser = AdventureGuideParser()
parser.process_pdf("guide.pdf", "./output/")

# Coordinate utilities
coords1 = Coordinates(59.9139, 10.7522, "N", "E")  # Oslo
coords2 = Coordinates(59.3293, 18.0686, "N", "E")  # Stockholm
distance = calculate_distance(coords1, coords2)     # 416.30 km
```

## 📁 Project Structure

```
find_your_next_adventure/          # Main package
├── models/                         # Data models (Coordinates, Destination, Chapter)
├── parsers/                        # PDF parsing (AdventureGuideParser)
├── utils/                          # Utilities (distance calc, formatting)
└── cli.py                          # Command-line interface

tests/                              # Comprehensive test suite
scripts/                            # Development utilities  
pdf_to_json_parser.py              # Legacy CLI
pyproject.toml                      # Modern packaging
Makefile                            # Development automation
```

## 🌍 Output Format

Generates JSON files organized by latitude ranges:
- `chapter_1_destinations.json` - Arctic (90°N to 60°N)  
- `chapter_2_destinations.json` - Northern (60°N to 45°N)
- `chapter_3_destinations.json` - Mid-northern (45°N to 30°N)
- `chapter_4_destinations.json` - Northern tropics (30°N to 15°N)
- `chapter_5_destinations.json` - Equatorial north (15°N to 0°)
- `chapter_6_destinations.json` - Equatorial south (0° to 15°S)
- `chapter_7_destinations.json` - Southern (15°S to 30°S)
- `chapter_8_destinations.json` - Antarctic (30°S to 90°S)
- `complete_adventure_guide.json` - Combined dataset

<details>
<summary>Example JSON Structure</summary>

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
        "latitude": 78.2232,
        "longitude": 15.6267,
        "latitudeDirection": "N",
        "longitudeDirection": "E"
      },
      "country": "Norway",
      "region": "Scandinavia"
    }
  ],
  "metadata": {
    "source": "Find Your Next Adventure Travel Guide",
    "chapter": "1",
    "generatedDate": "2025-08-01",
    "coordinateSystem": "WGS84"
  }
}
```
</details>
  "totalDestinations": 44,
  "destinations": [
    {
      "id": 1,
      "location": "Svalbard, Norway",
      "coordinates": {
        "latitude": 78.2232,
        "longitude": 15.6267,
        "latitudeDirection": "N",
        "longitudeDirection": "E"
      },
      "country": "Norway",
      "region": "Scandinavia"
    }
  ],
  "metadata": {
    "source": "Find Your Next Adventure Travel Guide",
    "chapter": "1",
    "generatedDate": "2025-08-01",
    "coordinateSystem": "WGS84",
    "format": "Decimal Degrees"
  }
}
```

## 🧪 Development

```bash
# Setup
make setup-dev              # Install dev dependencies + pre-commit hooks

# Testing  
make test                    # Run tests
make test-cov               # Run with coverage

# Code Quality
make format                 # Format code (black + isort)
make lint                   # Lint code (flake8)
make type-check            # Type checking (mypy)
make check                 # Run all checks

# Run example
make run-example
```

## 📋 Requirements & Standards

- **Python**: 3.8+ with full type hints
- **Dependencies**: PyMuPDF>=1.23.0, ollama>=0.1.0 (optional)
- **Code Style**: Black formatting, isort imports, flake8 linting
- **Architecture**: Modular design with comprehensive testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes following project standards
4. Run tests (`make check`)
5. Submit a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 📞 Support

- 🐛 [Issues](https://github.com/nicolas-marchand/find-your-next-adventure/issues)
- 📧 nicolas.marchand@example.com

---

**🎯 Ready for Professional Use | 🧪 Fully Tested | 📦 Modern Packaging**
