# Death Counter GUI

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey.svg)
![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)

Real-time death counter with graphical interface for FromSoftware games (Dark Souls, Elden Ring, Sekiro, Bloodborne, etc.)

## ✨ New Features

- **🖥️ Automatic screen detection**: Multi-monitor support with automatic resolution detection
- **🎨 Graphical interface**: Modern GUI compatible with Linux/Mac/Windows
- **⚙️ Flexible configuration**: Adjustable parameters via interface
- **📊 Real-time monitoring**: Live logs and status
- **🔧 Advanced debug mode**: Automatic screenshots during detections

## 🚀 Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Launch

### Linux/Mac
```bash
# Method 1: Launch script
./run_gui.sh

# Method 2: Direct
python3 death_counter_gui.py
```

### Windows
```batch
REM Method 1: Launch script
run_gui.bat

REM Method 2: Direct
python death_counter_gui.py
```

## 🎮 Usage

1. **Select screen**: Choose the screen where the game is displayed
2. **Configure zone**: Adjust capture zone dimensions
3. **Set parameters**:
   - **Scan delay**: Check frequency (in seconds)
   - **Verbose mode**: Shows all recognized text
   - **Debug mode**: Saves screenshots
4. **Test zone**: Button to test capture zone
5. **Start**: Launch monitoring

## 🔧 Configuration

### Automatic screen detection
- The program automatically detects your screens and their resolutions
- Basic multi-monitor support (simple detection for dual-screen setups)
- Selection via dropdown menu in interface

### Capture zone
- **Width**: 500-3000 pixels (default: 1500)
- **Height**: 100-800 pixels (default: 250)
- Zone automatically centered on selected screen

### Advanced parameters
- **OCR confidence threshold**: 0.4 (hard-coded, modifiable in code)
- **Supported messages**:
  - French: "VOUS ÊTES MORT" (Dark Souls), "VOUS AVEZ PÉRI" (Elden Ring)
  - English: "YOU DIED"
  - Common OCR variations

## 📁 Generated files

- `death_counter.json`: Saved death counter
- `death_counter_config.json`: Interface configuration
- `test_capture_*.png`: Zone test screenshots
- `death_screenshot_*.png`: Debug screenshots (if enabled)

## 🆚 Comparison with old version

| Feature | Old version | New GUI version |
|---|---|---|
| Interface | Terminal only | Modern GUI |
| Screen configuration | Hard-coded | Automatic detection |
| Multi-screen | Basic support | Selection via interface |
| Configuration | Code modification | Graphical interface |
| Logs | Terminal | Integrated log window |
| Zone testing | None | Test button |
| Config saving | None | Automatic |

## 🔧 Troubleshooting

### Common issues

1. **EasyOCR doesn't initialize**:
   - Check your internet connection (model downloads)
   - Verify you have enough disk space

2. **Incorrect screen detection**:
   - Multi-screen detection is simplified
   - You can manually modify screens in code if needed

3. **False positives/negatives**:
   - Adjust capture zone with "Test Zone" button
   - Enable verbose mode to see recognized text
   - Use debug mode to analyze captures

### Manual screen modification

If automatic detection doesn't work correctly, you can modify the `detect_screens()` method in the code:

```python
def detect_screens(self):
    # Example for 3 screens 1920x1080
    return [
        {
            'name': 'Main Screen',
            'origin': (0, 0),
            'resolution': (1920, 1080),
            'description': 'Main (1920x1080)'
        },
        {
            'name': 'Left Screen', 
            'origin': (-1920, 0),
            'resolution': (1920, 1080),
            'description': 'Left (1920x1080)'
        },
        {
            'name': 'Right Screen',
            'origin': (1920, 0),
            'resolution': (1920, 1080),
            'description': 'Right (1920x1080)'
        }
    ]
```

## 📝 Version

- **v1.0**: Initial stable release with GUI and terminal versions

## 📄 License

MIT License

## 👤 Author

[0xBAD5EED5]
