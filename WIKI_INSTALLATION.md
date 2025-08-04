# 🛠️ Installation & Setup Guide

Ready to start your adventure? Let's get everything set up! 🚀

## 📋 Prerequisites

### 🐍 Python Requirements
- **Python 3.8+** (3.11+ recommended)
- **pip** (Python package installer)

### 🤖 Ollama AI
- **Ollama** installed and running locally
- **phi4-mini** model (or your preferred model)

## 🚀 Quick Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/nmarchand73/find-your-next-adventure.git
cd find-your-next-adventure
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Start Ollama
```bash
# Install Ollama (if not already installed)
# Visit: https://ollama.ai/download

# Start Ollama service
ollama serve

# Pull the AI model (in a new terminal)
ollama pull phi4-mini
```

### Step 4: Test Your Setup
```bash
python run.py
```

🎉 **You should see the program start processing the sample PDF!**

## 🔧 Detailed Setup

### 🐍 Python Environment (Recommended)

#### Option A: Virtual Environment
```bash
# Create virtual environment
python -m venv adventure_env

# Activate (Windows)
adventure_env\Scripts\activate

# Activate (macOS/Linux)
source adventure_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option B: Conda Environment
```bash
# Create conda environment
conda create -n adventure_env python=3.11

# Activate environment
conda activate adventure_env

# Install dependencies
pip install -r requirements.txt
```

### 🤖 Ollama Setup

#### 1. Install Ollama
- **Windows**: Download from [ollama.ai](https://ollama.ai/download)
- **macOS**: `brew install ollama`
- **Linux**: `curl -fsSL https://ollama.ai/install.sh | sh`

#### 2. Start Ollama Service
```bash
ollama serve
```

#### 3. Pull AI Model
```bash
# Default model (recommended)
ollama pull phi4-mini

# Alternative models (optional)
ollama pull llama3.2:3b
ollama pull mistral:7b
```

#### 4. Verify Ollama is Running
```bash
# Test Ollama connection
curl http://localhost:11434/api/tags
```

### 📦 Dependencies Breakdown

#### Core Dependencies
- **PyMuPDF**: PDF text extraction
- **ollama**: AI model integration
- **httpx**: HTTP client for API calls
- **dataclasses**: Data structure support

#### Development Dependencies
- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Linting
- **coverage**: Test coverage

## 🎯 Configuration Options

### 🤖 AI Model Configuration

Edit `find_your_next_adventure/utils/ollama_generator.py`:

```python
# Change the model
self.model = "llama3.2:3b"  # or "mistral:7b"

# Adjust batch processing
self.batch_size = 10  # Process more locations at once

# Control AI creativity
self.options = {
    'temperature': 0.8,  # Higher = more creative
    'max_tokens': 300,   # Longer descriptions
}
```

### 📊 Logging Configuration

Edit `find_your_next_adventure/utils/logging_config.py`:

```python
# Change log file location
setup_logging(log_file="my_custom_log.log")

# Adjust log level
setup_logging(log_level=logging.DEBUG)

# Disable console output
setup_logging(console_output=False)
```

### 🌍 Geographic Configuration

Edit `find_your_next_adventure/parsers/adventure_guide_parser.py`:

```python
# Add new countries
COUNTRY_MAPPING = {
    "NEW_COUNTRY": {"country": "New Country", "region": "New Region"},
    # ... existing mappings
}

# Add special cases
SPECIAL_CASES = {
    "UNIQUE_LOCATION": {"country": "Special Country", "region": "Special Region"},
    # ... existing cases
}
```

## 🔍 Troubleshooting

### ❌ Common Issues

#### 1. Ollama Connection Error
```
Error: Connection refused to Ollama service
```
**Solution:**
```bash
# Start Ollama service
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

#### 2. Model Not Found
```
Error: Model 'phi4-mini' not found
```
**Solution:**
```bash
# Pull the model
ollama pull phi4-mini

# List available models
ollama list
```

#### 3. PDF Processing Error
```
Error: Failed to load PDF content
```
**Solution:**
- Ensure PDF is not corrupted
- Check file permissions
- Verify PDF contains text (not just images)

#### 4. Memory Issues
```
Error: Out of memory during processing
```
**Solution:**
```python
# Reduce batch size in ollama_generator.py
self.batch_size = 3  # Smaller batches
```

### 🔧 Performance Optimization

#### For Large PDFs
```python
# Increase batch size for efficiency
self.batch_size = 10

# Use faster model
self.model = "phi4-mini"  # Smaller, faster model
```

#### For Better AI Quality
```python
# Use larger model for better descriptions
self.model = "llama3.2:3b"

# Increase creativity
self.options = {
    'temperature': 0.9,
    'max_tokens': 400,
}
```

## 🧪 Testing Your Installation

### 1. Basic Functionality Test
```bash
python run.py
```
**Expected Output:**
- PDF loading progress
- AI processing messages
- Generated JSON files in `output/` directory

### 2. Custom PDF Test
```bash
python run.py "your_test_pdf.pdf" "./test_output/"
```

### 3. AI Model Test
```python
# Test Ollama connection
from find_your_next_adventure.utils.ollama_generator import OllamaGenerator

generator = OllamaGenerator()
if generator.test_connection():
    print("✅ Ollama connection successful!")
else:
    print("❌ Ollama connection failed!")
```

## 📊 System Requirements

### Minimum Requirements
- **RAM**: 4GB (8GB recommended)
- **Storage**: 2GB free space
- **CPU**: Dual-core processor
- **Network**: Internet connection for initial setup

### Recommended Requirements
- **RAM**: 16GB for large PDFs
- **Storage**: 10GB free space
- **CPU**: Quad-core processor
- **GPU**: Optional (for faster AI processing)

## 🎉 Next Steps

Once installation is complete:

1. **Try the sample**: `python run.py`
2. **Process your own PDF**: `python run.py "your_pdf.pdf" "./output/"`
3. **Customize settings**: Edit configuration files
4. **Explore output**: Check generated JSON files
5. **Integrate**: Use JSON data in your applications

---

*🚀 Ready to transform your travel guides into intelligent adventure data!* 