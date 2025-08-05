# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-08-05

### 🎉 Initial Release

**Death Counter** is a real-time OCR-based death counter for FromSoftware games that automatically detects and counts player deaths.

### ✨ Features

#### Core Functionality
- **Real-time OCR monitoring** using EasyOCR for death message detection
- **Automatic death counting** with persistent storage in JSON format
- **Multi-language support** for French and English death messages
- **Cross-platform compatibility** (Linux, macOS, Windows)

#### Supported Games & Messages
- **Dark Souls series**: "YOU DIED" (EN), "VOUS ÊTES MORT" (FR)
- **Elden Ring**: "YOU DIED" (EN), "VOUS AVEZ PÉRI" (FR) 
- **Sekiro, Bloodborne**: "YOU DIED" (EN)
- **OCR error tolerance** with text similarity matching for recognition variations

#### GUI Application (`death_counter_gui.py`)
- **Modern tkinter-based interface** with intuitive controls
- **Automatic screen detection** with multi-monitor support
- **Configurable capture zone** (500-3000px width, 100-800px height)
- **Real-time monitoring status** with live logs and counter display
- **Test capture functionality** to verify screen capture zone
- **Flexible scan settings** (0.1-5.0 second intervals)
- **Debug mode** with automatic screenshot saving when deaths detected
- **Verbose logging** option to see all recognized text
- **Persistent configuration** automatically saved to JSON

#### Terminal Version (`death_counter.py`)
- **Lightweight command-line interface** for minimal resource usage
- **Configurable parameters** via code modification
- **Console output** with death detection notifications
- **Background monitoring** with keyboard interrupt support

#### Technical Features
- **Image preprocessing** with contrast/sharpness enhancement for better OCR accuracy
- **Centered capture zones** automatically calculated for each screen
- **Thread-safe GUI updates** using tkinter's after() method
- **Error handling** for screen capture and OCR processing failures
- **JSON-based data persistence** for counter and configuration storage

### 📦 Installation & Distribution
- **pip-installable package** with setuptools configuration
- **Console entry points** for easy command-line access
- **Requirements specification** with pinned dependency versions
- **Launch scripts** provided for Windows (.bat) and Unix (.sh)

### 📚 Documentation
- **Comprehensive README** with installation and usage instructions
- **API documentation** covering all functions and classes
- **Usage guide** with configuration options and troubleshooting
- **Development guide** for contributors and advanced users
- **Contributing guidelines** with code style and PR process

### 🔧 Configuration Options
- **Screen selection** from auto-detected displays
- **Capture zone dimensions** with live preview
- **OCR confidence threshold** (0.4 default)
- **Monitoring frequency** adjustable from 0.1 to 5.0 seconds
- **Debug screenshot saving** for analysis
- **Verbose output** for development and troubleshooting

### 📁 Project Structure
```
DeathCounter-py/
├── src/                    # Source code
│   ├── death_counter_gui.py   # GUI application
│   ├── death_counter.py       # Terminal version
│   └── __init__.py            # Package initialization
├── scripts/                   # Launch utilities
├── docs/                      # Documentation
├── requirements.txt           # Dependencies
└── setup.py                  # Package configuration
```

### 🎯 Technical Specifications
- **Python version**: 3.8+ supported (tested up to 3.12)
- **Key dependencies**: 
  - EasyOCR 1.6.0+ for text recognition
  - Pillow 9.0.0+ for image processing
  - NumPy 1.21.0+ for array operations
  - tkinter (included with Python) for GUI
- **OCR languages**: English (`en`) and French (`fr`)
- **Supported platforms**: Linux, macOS, Windows
- **License**: MIT License