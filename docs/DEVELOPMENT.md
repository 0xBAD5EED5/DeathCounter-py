# Death Counter - Developer Guide

## 🏗️ Architecture Overview

### Core Components
- **OCR Engine**: EasyOCR for text recognition
- **Screen Capture**: PIL/Pillow for screenshot functionality  
- **GUI Framework**: tkinter for cross-platform interface
- **Data Persistence**: JSON for configuration and counter storage

### Project Structure
```
DeathCounter-py/
├── src/                    # Source code
│   ├── __init__.py        # Package initialization
│   ├── death_counter.py   # Terminal version
│   └── death_counter_gui.py # GUI version
├── scripts/               # Launch scripts
│   ├── run_gui.sh        # Linux/Mac launcher
│   └── run_gui.bat       # Windows launcher
├── assets/               # Resources and screenshots
├── docs/                 # Documentation
├── requirements.txt      # Python dependencies
├── setup.py             # Package configuration
└── README.md            # Project overview
```

## 🔧 Development Environment

### Prerequisites
- Python 3.8+ (tested with 3.12)
- pip package manager
- Virtual environment (recommended)

### Setup
```bash
# Clone repository
git clone <your-repo-url>
cd DeathCounter-py

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Development install
pip install -e .
```

### Development Dependencies
Add to `requirements-dev.txt` for development:
```
pytest>=7.0.0
black>=22.0.0
flake8>=5.0.0
mypy>=0.991
```

## 🏃‍♂️ Running & Testing

### Running Applications
```bash
# GUI version
python src/death_counter_gui.py

# Terminal version
python src/death_counter.py

# Using launch scripts
./scripts/run_gui.sh      # Linux/Mac
scripts\run_gui.bat       # Windows
```

### Testing
Currently manual testing. To add automated tests:

```bash
# Create tests directory
mkdir tests
touch tests/__init__.py
touch tests/test_death_counter.py
```

Example test structure:
```python
import unittest
from src.death_counter_gui import DeathCounterGUI

class TestDeathCounter(unittest.TestCase):
    def test_similarity_calculation(self):
        # Test text similarity function
        pass
    
    def test_screen_detection(self):
        # Test screen detection logic
        pass
```

## 🎯 Core Functions

### Text Recognition Pipeline
```python
def is_death_message_detected(image, reader, verbose=False):
    """
    Detects death messages in game screenshots
    
    Args:
        image: PIL Image object
        reader: EasyOCR Reader instance
        verbose: Enable detailed logging
    
    Returns:
        bool: True if death message detected
    """
```

### Screen Capture
```python
def capture_screen_zone(origin, zone_size):
    """
    Captures specific screen region
    
    Args:
        origin: (x, y) screen coordinates
        zone_size: (width, height) capture dimensions
    
    Returns:
        PIL.Image: Screenshot of specified region
    """
```

### Configuration Management
```python
def save_config(config_data, filename="death_counter_config.json"):
    """Saves configuration to JSON file"""
    
def load_config(filename="death_counter_config.json"):
    """Loads configuration from JSON file"""
```

## 🔍 Adding New Game Support

### Step 1: Identify Death Messages
Research the exact text displayed when player dies:
- Different languages (English, French, etc.)
- Different game versions
- Case sensitivity and punctuation

### Step 2: Add Message Patterns
Edit the message detection list in both versions:

```python
# In death_counter.py and death_counter_gui.py
death_messages = [
    "YOU DIED",           # Dark Souls, Elden Ring (EN)
    "VOUS ÊTES MORT",     # Dark Souls (FR)
    "VOUS AVEZ PÉRI",     # Elden Ring (FR)
    "NEW_GAME_MESSAGE",   # Add here
]
```

### Step 3: Test & Validate
- Use verbose mode to see recognized text
- Test with different screen resolutions
- Verify no false positives with similar game text

### Step 4: Update Documentation
- Add to supported games list
- Update README.md and USAGE.md
- Include example screenshots if possible

## 🎨 GUI Development

### Layout Structure
```
MainWindow
├── ConfigFrame (top)
│   ├── ScreenSelector
│   ├── ZoneConfigFrame
│   └── ControlButtons
├── StatusFrame (middle)
│   ├── CounterDisplay
│   └── StatusText  
└── LogFrame (bottom)
    └── ScrollableLog
```

### Key GUI Components
```python
class DeathCounterGUI:
    def __init__(self):
        self.setup_gui()
        self.load_config()
    
    def setup_gui(self):
        """Initialize GUI components"""
    
    def update_gui(self):
        """Update GUI elements (called by timer)"""
    
    def start_monitoring(self):
        """Begin death detection loop"""
```

### Threading Considerations
- OCR processing runs in main thread (tkinter limitation)
- Use `self.root.after()` for periodic tasks
- Avoid blocking operations in GUI thread

## 🔧 Configuration System

### Config File Format
```json
{
    "selected_screen_name": "Primary (1920x1080)",
    "capture_width": 1500,
    "capture_height": 250,
    "scan_delay": 1.0,
    "verbose_mode": false,
    "debug_mode": false,
    "window_geometry": "800x600+100+100"
}
```

### Adding New Config Options
1. Add to default config in GUI class
2. Update save/load functions
3. Add GUI controls if needed
4. Document in USAGE.md

## 🐛 Debugging & Troubleshooting

### Debug Mode Features
- Saves screenshots when deaths detected
- Timestamps all debug images
- Verbose OCR output to console

### Common Development Issues

#### OCR Not Working
```python
# Check EasyOCR installation
import easyocr
reader = easyocr.Reader(['en', 'fr'])
result = reader.readtext(image)
print(result)  # Debug OCR output
```

#### Screen Capture Issues
```python
# Test screen capture
from PIL import ImageGrab
image = ImageGrab.grab(bbox=(x, y, x+width, y+height))
image.save("debug_capture.png")
```

#### GUI Threading Problems
```python
# Use after() instead of direct calls
self.root.after(100, self.update_function)
# Not: self.update_function()
```

## 📦 Building & Distribution

### Creating Executable
Using PyInstaller:
```bash
pip install pyinstaller

# GUI version
pyinstaller --onefile --windowed src/death_counter_gui.py

# Terminal version  
pyinstaller --onefile src/death_counter.py
```

### Package Distribution
```bash
# Build package
python setup.py sdist bdist_wheel

# Install locally
pip install dist/death-counter-*.whl

# Upload to PyPI (when ready)
pip install twine
twine upload dist/*
```

## 🔄 Version Management

### Semantic Versioning
- **Major**: Breaking changes (2.0.0)
- **Minor**: New features (1.1.0)  
- **Patch**: Bug fixes (1.0.1)

### Release Process
1. Update version in `setup.py`
2. Update `CHANGELOG.md`
3. Create git tag: `git tag v1.0.1`
4. Build and test package
5. Create GitHub release

## 🤝 Contributing Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

### Pull Request Process
1. Fork repository
2. Create feature branch
3. Make changes with tests
4. Update documentation
5. Submit pull request

### Issue Reporting
Include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if GUI related

## 📚 Learning Resources

### OCR & Computer Vision
- [EasyOCR Documentation](https://github.com/JaidedAI/EasyOCR)
- [PIL/Pillow Guide](https://pillow.readthedocs.io/)

### GUI Development
- [tkinter Tutorial](https://docs.python.org/3/library/tkinter.html)
- [GUI Best Practices](https://wiki.python.org/moin/TkInter)

### Game Development
- [Screen Capture Techniques](https://python-forum.io/thread-21277.html)
- [Real-time Processing](https://realpython.com/python-gui-tkinter/)
