# Death Counter - Usage Guide

## 🚀 Quick Start

### GUI Version (Recommended)
1. **Launch**: Run `python src/death_counter_gui.py` or use launch scripts
2. **Configure**: Select your screen and adjust capture zone
3. **Test**: Use "Test Zone" button to verify capture area
4. **Start**: Click "Start" to begin monitoring

### Terminal Version
1. **Configure**: Edit variables in `src/death_counter.py` if needed
2. **Launch**: Run `python src/death_counter.py`
3. **Monitor**: Watch console output for death detections

## ⚙️ Configuration Options

### Screen Selection
- **Auto-detection**: Program detects available screens
- **Manual selection**: Choose from dropdown in GUI
- **Multi-monitor**: Works with dual/triple monitor setups

### Capture Zone
- **Width**: 500-3000 pixels (default: 1500)
- **Height**: 100-800 pixels (default: 250)  
- **Position**: Automatically centered on selected screen
- **Test**: Use "Test Zone" to save a screenshot of capture area

### Detection Settings
- **Scan Delay**: 0.1-5.0 seconds between checks (default: 1.0)
- **Confidence**: OCR confidence threshold (0.4, hard-coded)
- **Verbose Mode**: Shows all recognized text in logs
- **Debug Mode**: Saves screenshots when deaths are detected

## 🎮 Supported Games & Messages

### Dark Souls Series
- **French**: "VOUS ÊTES MORT"
- **English**: "YOU DIED"

### Elden Ring
- **French**: "VOUS AVEZ PÉRI"
- **English**: "YOU DIED"

### Sekiro, Bloodborne
- **English**: "YOU DIED"

## 🔧 Advanced Usage

### Custom Screen Configuration
If auto-detection doesn't work, modify `detect_screens()` in GUI version:

```python
def detect_screens(self):
    return [
        {
            'name': 'Gaming Monitor',
            'origin': (1920, 0),  # X, Y offset
            'resolution': (2560, 1440),  # Width, Height
            'description': 'Gaming (2560x1440)'
        }
    ]
```

### Performance Optimization
- **Smaller capture zone**: Faster processing
- **Higher scan delay**: Less CPU usage
- **Close unnecessary programs**: Better OCR performance

### Troubleshooting Detection
1. **Enable verbose mode**: See what text is recognized
2. **Enable debug mode**: Analyze saved screenshots
3. **Adjust capture zone**: Ensure death message is in center
4. **Check resolution**: Works best with 1080p+ displays

## 📁 File Locations

### Generated Files
- `death_counter.json`: Saved death count
- `death_counter_config.json`: GUI settings
- `test_capture_*.png`: Test screenshots
- `death_screenshot_*.png`: Debug screenshots (timestamped)

### Configuration Files
- `src/death_counter.py`: Terminal version settings
- GUI settings: Saved automatically in JSON

## 🎯 Tips for Best Results

### Game Setup
- **Windowed/Borderless**: Often works better than fullscreen
- **UI Scale**: Default game UI scaling recommended
- **Language**: French/English supported (message language, not game language)

### Monitor Setup
- **Primary display**: Usually most reliable
- **Resolution**: 1080p or higher recommended
- **Scaling**: 100% display scaling preferred

### Performance
- **Close overlays**: Discord, Steam overlay, etc.
- **Stable framerate**: Helps with consistent text rendering
- **Good lighting**: In-game brightness doesn't affect OCR

## 🐛 Common Issues

### "No death messages detected"
- Check capture zone covers death message area
- Enable verbose mode to see recognized text
- Try different scan delay (0.5-2.0 seconds)

### "False positive detections"
- Reduce capture zone to exclude UI elements
- Check for similar text in game (merchant names, etc.)
- Adjust confidence threshold in code if needed

### "Application crashes"
- Check Python version (3.8+ required)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check available disk space (EasyOCR needs space for models)

### "Screen not detected correctly"
- Use manual screen configuration (see Advanced Usage)
- Check display arrangement in OS settings
- Try different monitor as primary

## 📊 Statistics & Data

### Counter Persistence
- Automatically saved after each death
- Survives application restarts
- Stored in JSON format for easy editing

### Reset Options
- GUI: "Reset" button with confirmation
- Manual: Delete or edit `death_counter.json`
- Backup: Copy JSON file before major gaming sessions

## 🔄 Updates & Maintenance

### Keeping Updated
- Check GitHub releases for new versions
- Update dependencies: `pip install -r requirements.txt --upgrade`
- Review CHANGELOG.md for new features

### Contributing Data
- Report false positives/negatives as GitHub issues
- Share screenshots of undetected death messages
- Suggest new game support with message examples
