# 🏗️ Technical Architecture

Welcome to the technical deep-dive! Let's explore how **Find Your Next Adventure** works under the hood. 🔧

## 🎯 System Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   📄 PDF Input  │───▶│  🔍 Parser      │───▶│  🤖 AI Engine   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  🌍 Geographic   │    │  📊 Logging     │
                       │   Intelligence   │    │   System        │
                       └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  🗺️ Maps &      │    │  📁 JSON        │
                       │   Links Gen     │    │   Output        │
                       └─────────────────┘    └─────────────────┘
```

## 🧩 Core Components

### 📖 PDF Parser (`adventure_guide_parser.py`)

**Purpose**: Extracts structured data from PDF adventure guides

**Key Features**:
- **Regex Pattern Matching**: `(\d+)\.\s+(.+?)\s+-\s+Latitude:\s*([\d.-]+)\s*([NS])\s+Longitude:\s*([\d.-]+)\s*([EW])?`
- **Coordinate Validation**: Ensures latitude (-90 to 90) and longitude (-180 to 180)
- **Country Mapping**: 200+ countries and regions automatically identified
- **Special Cases**: Handles unique locations like "Both Poles" or "Worldwide"

**Data Flow**:
```
PDF Text → Regex Match → Coordinate Parse → Country ID → Destination Object
```

### 🤖 AI Generator (`ollama_generator.py`)

**Purpose**: Enhances destinations with AI-generated descriptions

**Key Features**:
- **Batch Processing**: Processes 5 locations simultaneously for efficiency
- **Bilingual Output**: English and French descriptions
- **Smart Fallbacks**: Graceful error handling with meaningful defaults
- **Connection Testing**: Verifies Ollama service availability

**Processing Flow**:
```
Location → Batch Queue → AI Prompt → Response Parse → Bilingual Output
```

### 🌍 Geographic Intelligence

**Country Mapping System**:
```python
COUNTRY_MAPPING = {
    "NORWAY": {"country": "Norway", "region": "Scandinavia"},
    "JAPAN": {"country": "Japan", "region": "East Asia"},
    # ... 200+ countries
}
```

**Special Cases Handling**:
```python
SPECIAL_CASES = {
    "BOTH POLES": {"country": "Multiple", "region": "Global"},
    "WORLDWIDE": {"country": "Multiple", "region": "Global"},
    # ... unique locations
}
```

### 📊 Logging System (`logging_config.py`)

**Purpose**: Centralized logging with console and file output

**Features**:
- **Rotating File Handler**: 10MB max, 5 backup files
- **Console + File Output**: Real-time progress + persistent logs
- **Session Tracking**: Start/end markers with statistics
- **Module Identification**: Each log entry shows source module

**Log Levels**:
- **INFO**: Progress updates, successful operations
- **WARNING**: Non-critical issues, fallbacks used
- **ERROR**: Critical failures, processing errors

## 🔄 Data Flow Architecture

### 1. PDF Processing Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   PDF File  │───▶│  PyMuPDF    │───▶│  Text Lines │
└─────────────┘    └─────────────┘    └─────────────┘
                          │
                          ▼
                   ┌─────────────┐    ┌─────────────┐
                   │  Regex      │───▶│  Parsed     │
                   │  Matching   │    │  Locations  │
                   └─────────────┘    └─────────────┘
```

### 2. AI Enhancement Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Location   │───▶│  Batch      │───▶│  Ollama     │
│  Data       │    │  Queue      │    │  AI Call    │
└─────────────┘    └─────────────┘    └─────────────┘
                          │                    │
                          ▼                    ▼
                   ┌─────────────┐    ┌─────────────┐
                   │  Response   │◀───│  AI         │
                   │  Parser     │    │  Response   │
                   └─────────────┘    └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │  Bilingual  │
                   │  Descriptions│
                   └─────────────┘
```

### 3. Output Generation Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Enhanced   │───▶│  Geographic  │───▶│  JSON       │
│  Destinations│   │  Grouping    │    │  Generation │
└─────────────┘    └─────────────┘    └─────────────┘
                          │                    │
                          ▼                    ▼
                   ┌─────────────┐    ┌─────────────┐
                   │  Chapter    │    │  Individual │
                   │  Files      │    │  Files      │
                   └─────────────┘    └─────────────┘
```

## 🏛️ Data Models

### 📍 Destination Model
```python
@dataclass
class Destination:
    id: int
    location: str
    coordinates: Coordinates
    country: str
    region: str
    mainAttractionEn: str
    mainAttractionFr: str
    googleMapsLink: str
    extendedLinks: ExtendedLinks
```

### 🌍 Coordinates Model
```python
@dataclass
class Coordinates:
    latitude: float
    longitude: float
    latitudeDirection: str
    longitudeDirection: str
```

### 📚 Chapter Model
```python
@dataclass
class Chapter:
    title: str
    description: str
    latitudeRange: dict
    totalDestinations: int
    destinations: List[Destination]
    metadata: dict
```

## 🔧 Configuration Architecture

### 🤖 AI Configuration
```python
class OllamaGenerator:
    def __init__(self, model="phi4-mini", batch_size=5):
        self.model = model
        self.batch_size = batch_size
        self.options = {
            'temperature': 0.7,
            'max_tokens': 200
        }
```

### 📊 Logging Configuration
```python
def setup_logging(
    log_file="find_your_next_adventure.log",
    log_level=logging.INFO,
    max_bytes=10*1024*1024,  # 10MB
    backup_count=5,
    console_output=True
):
```

### 🌍 Geographic Configuration
```python
CHAPTERS = {
    1: {"title": "From 90° North to 60° North", "ids": (1, 44)},
    2: {"title": "From 60° North to 45° North", "ids": (45, 265)},
    # ... 8 chapters total
}
```

## 🚀 Performance Optimizations

### 🎯 Batch Processing
- **Efficiency**: Process 5 locations per AI call
- **Memory Management**: Queue-based processing
- **Error Isolation**: Individual location failures don't stop batch

### 📊 Smart Caching
- **Batch Results**: Store AI responses for retrieval
- **Session Persistence**: Maintain state across processing
- **Fallback System**: Graceful degradation on AI failures

### 🔄 Asynchronous Design
- **Non-blocking**: PDF parsing continues during AI processing
- **Queue Management**: Efficient batch queue handling
- **Resource Management**: Proper cleanup and memory management

## 🛡️ Error Handling Strategy

### 🎯 Graceful Degradation
```python
try:
    # AI processing
    response = ollama.generate(...)
except Exception as e:
    # Fallback to default descriptions
    fallback_en = f"Discover the unique charm of {location}."
    fallback_fr = f"Découvrez le charme unique de {location}."
```

### 📊 Comprehensive Logging
- **Session Tracking**: Complete audit trail
- **Error Context**: Detailed error information
- **Performance Metrics**: Success rates and timing

### 🔍 Debug Support
- **Failed Lines**: Track parsing failures
- **Debug Reports**: JSON files with error details
- **Progress Tracking**: Real-time processing status

## 🌐 Integration Points

### 🗺️ External Services
- **Google Maps**: Coordinate-based link generation
- **Booking.com**: Travel booking links
- **TripAdvisor**: Review and recommendation links
- **Wikipedia**: Information links

### 🤖 AI Services
- **Ollama**: Local AI processing
- **HTTP API**: RESTful communication
- **Model Management**: Dynamic model switching

### 📁 File System
- **PDF Input**: PyMuPDF processing
- **JSON Output**: Structured data files
- **Log Files**: Rotating log management

## 🔮 Future Architecture Considerations

### 🚀 Scalability Enhancements
- **Distributed Processing**: Multi-node AI processing
- **Database Integration**: Persistent storage for large datasets
- **API Endpoints**: RESTful API for external access

### 🌍 Geographic Enhancements
- **Advanced Mapping**: More sophisticated country detection
- **Regional Intelligence**: Cultural and seasonal considerations
- **Multi-language**: Support for additional languages

### 🤖 AI Enhancements
- **Model Selection**: Dynamic model choosing
- **Quality Scoring**: AI output quality assessment
- **Custom Training**: Domain-specific model fine-tuning

---

*🏗️ Built with clean architecture principles for scalability, maintainability, and performance!* 