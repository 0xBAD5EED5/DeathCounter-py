# Death Counter - API Reference

## 📋 Table of Contents
- [Core Functions](#core-functions)
- [GUI Classes](#gui-classes)
- [Configuration](#configuration)
- [Screen Management](#screen-management)
- [Data Persistence](#data-persistence)
- [Utilities](#utilities)

---

## 🔧 Core Functions

### `is_death_message_detected(image, reader, verbose=False)`
**Purpose**: Detects death messages in game screenshots using OCR

**Parameters**:
- `image` (PIL.Image): Screenshot image to analyze
- `reader` (easyocr.Reader): Initialized EasyOCR reader instance
- `verbose` (bool, optional): Enable detailed logging output

**Returns**:
- `bool`: True if death message detected, False otherwise

**Example**:
```python
import easyocr
from PIL import Image

reader = easyocr.Reader(['en', 'fr'])
image = Image.open('screenshot.png')
is_death = is_death_message_detected(image, reader, verbose=True)
```

**Supported Messages**:
- "YOU DIED" (English - Dark Souls, Elden Ring, Sekiro, Bloodborne)
- "VOUS ÊTES MORT" (French - Dark Souls series)
- "VOUS AVEZ PÉRI" (French - Elden Ring)

---

### `calculate_text_similarity(text1, text2)`
**Purpose**: Calculates similarity between two text strings using difflib

**Parameters**:
- `text1` (str): First text string
- `text2` (str): Second text string

**Returns**:
- `float`: Similarity ratio between 0.0 and 1.0

**Example**:
```python
similarity = calculate_text_similarity("YOU DIED", "Y0U DIED")
# Returns: ~0.89 (high similarity despite OCR error)
```

**Note**: Used to handle OCR recognition errors and variations

---

### `capture_screen_zone(origin, zone_size)`
**Purpose**: Captures a specific rectangular region of the screen

**Parameters**:
- `origin` (tuple): (x, y) coordinates of top-left corner
- `zone_size` (tuple): (width, height) dimensions of capture area

**Returns**:
- `PIL.Image`: Screenshot of specified region

**Example**:
```python
# Capture center of 1920x1080 screen
origin = (210, 415)  # Centered position
zone_size = (1500, 250)  # Capture dimensions
screenshot = capture_screen_zone(origin, zone_size)
```

---

## 🖥️ GUI Classes

### `class DeathCounterGUI`
**Purpose**: Main GUI application class for death counter

#### `__init__(self)`
**Purpose**: Initialize GUI application

**Side Effects**:
- Creates main window
- Loads configuration
- Initializes OCR reader
- Sets up GUI components

#### `setup_gui(self)`
**Purpose**: Creates and arranges GUI elements

**Components Created**:
- Screen selection dropdown
- Zone configuration controls
- Start/Stop/Reset buttons
- Counter display
- Log output area

#### `detect_screens(self)`
**Purpose**: Auto-detects available display screens

**Returns**:
- `list`: Array of screen dictionaries

**Screen Dictionary Format**:
```python
{
    'name': 'Primary (1920x1080)',
    'origin': (0, 0),
    'resolution': (1920, 1080),
    'description': 'Primary (1920x1080)'
}
```

#### `update_capture_zone(self)`
**Purpose**: Recalculates capture zone based on current settings

**Side Effects**:
- Updates `self.capture_origin`
- Updates `self.capture_zone_size`
- Centers zone on selected screen

#### `start_monitoring(self)`
**Purpose**: Begins death detection monitoring loop

**Side Effects**:
- Changes GUI state to "monitoring"
- Starts periodic OCR checks
- Updates status display

#### `stop_monitoring(self)`
**Purpose**: Stops death detection monitoring

**Side Effects**:
- Changes GUI state to "stopped"
- Cancels periodic tasks
- Updates status display

#### `test_capture_zone(self)`
**Purpose**: Tests current capture zone and saves screenshot

**Side Effects**:
- Captures test screenshot
- Saves as `test_capture_{timestamp}.png`
- Updates log with results

#### `reset_counter(self)`
**Purpose**: Resets death counter to zero with confirmation

**Side Effects**:
- Shows confirmation dialog
- Resets counter if confirmed
- Updates display and saves data

---

## ⚙️ Configuration

### Configuration File Format
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

### `save_config(config_data, filename="death_counter_config.json")`
**Purpose**: Saves configuration dictionary to JSON file

**Parameters**:
- `config_data` (dict): Configuration data to save
- `filename` (str, optional): Config file name

**Example**:
```python
config = {
    "capture_width": 1500,
    "capture_height": 250,
    "scan_delay": 1.0
}
save_config(config)
```

### `load_config(filename="death_counter_config.json")`
**Purpose**: Loads configuration from JSON file

**Parameters**:
- `filename` (str, optional): Config file name

**Returns**:
- `dict`: Configuration data, or default config if file not found

---

## 🖼️ Screen Management

### Screen Detection
Auto-detects screens using `tkinter.winfo_screenwidth()` and `tkinter.winfo_screenheight()`

**Primary Screen**:
- Origin: (0, 0)
- Resolution: System-detected

**Multi-Monitor Setup**:
Currently supports primary screen. For multi-monitor, manual configuration required:

```python
def detect_screens(self):
    return [
        {
            'name': 'Primary (1920x1080)',
            'origin': (0, 0),
            'resolution': (1920, 1080),
            'description': 'Primary (1920x1080)'
        },
        {
            'name': 'Secondary (2560x1440)',
            'origin': (1920, 0),
            'resolution': (2560, 1440),
            'description': 'Secondary (2560x1440)'
        }
    ]
```

### Capture Zone Calculation
```python
def calculate_zone_position(screen_resolution, zone_size):
    """Centers capture zone on screen"""
    x = (screen_resolution[0] - zone_size[0]) // 2
    y = (screen_resolution[1] - zone_size[1]) // 2
    return (x, y)
```

---

## 💾 Data Persistence

### Death Counter Storage
**File**: `death_counter.json`
**Format**:
```json
{
    "count": 42
}
```

### `save_death_count(count)`
**Purpose**: Saves current death count to JSON file

**Parameters**:
- `count` (int): Current death count

### `load_death_count()`
**Purpose**: Loads death count from JSON file

**Returns**:
- `int`: Saved death count, or 0 if file not found

---

## 🛠️ Utilities

### `log_message(text, log_widget=None)`
**Purpose**: Logs message to console and optionally to GUI

**Parameters**:
- `text` (str): Message to log
- `log_widget` (tkinter.Text, optional): GUI log widget

**Example**:
```python
log_message("Death detected!", self.log_text_widget)
```

### `get_timestamp()`
**Purpose**: Returns current timestamp string

**Returns**:
- `str`: Formatted timestamp (YYYY-MM-DD_HH-MM-SS)

**Example**:
```python
timestamp = get_timestamp()
# Returns: "2024-01-15_14-30-25"
```

### `create_debug_screenshot(image, prefix="death_screenshot")`
**Purpose**: Saves debug screenshot with timestamp

**Parameters**:
- `image` (PIL.Image): Image to save
- `prefix` (str, optional): Filename prefix

**Side Effects**:
- Saves image as `{prefix}_{timestamp}.png`

---

## 🔍 OCR Configuration

### EasyOCR Reader Setup
```python
import easyocr

# Initialize reader with language support
reader = easyocr.Reader(['en', 'fr'])  # English and French

# Optional parameters for better performance
reader = easyocr.Reader(
    ['en', 'fr'],
    gpu=False,  # CPU-only mode
    verbose=False  # Disable download progress
)
```

### OCR Result Format
```python
# EasyOCR returns list of tuples
results = reader.readtext(image)
# Format: [(bbox, text, confidence), ...]

# Example result:
[
    ([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], 'YOU DIED', 0.89),
    ([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], 'Press any key', 0.76)
]
```

### Confidence Threshold
Current threshold: `0.4` (40% confidence minimum)

**Adjusting Threshold**:
```python
def is_death_message_detected(image, reader, verbose=False, min_confidence=0.4):
    results = reader.readtext(image)
    for (bbox, text, confidence) in results:
        if confidence >= min_confidence:
            # Process high-confidence text
```

---

## 🚨 Error Handling

### Common Exceptions

#### `ImportError`
```python
try:
    import easyocr
except ImportError:
    print("Please install EasyOCR: pip install easyocr")
    sys.exit(1)
```

#### `PIL.UnidentifiedImageError`
```python
try:
    image = ImageGrab.grab(bbox=capture_bbox)
except Exception as e:
    log_message(f"Screen capture failed: {e}")
    return False
```

#### `FileNotFoundError` (Config/Data)
```python
def load_config(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return get_default_config()
```

---

## 📊 Performance Considerations

### OCR Optimization
- **Smaller capture zones**: Faster processing
- **Higher scan delays**: Reduced CPU usage
- **Image preprocessing**: Enhance text clarity

### Memory Management
- Images are processed and discarded immediately
- No persistent image storage (except debug mode)
- OCR reader reused across detections

### Threading
- GUI runs in main thread (tkinter requirement)
- OCR processing is synchronous
- Use `root.after()` for periodic tasks

**Example Timing**:
```python
def check_for_death(self):
    start_time = time.time()
    # ... OCR processing ...
    processing_time = time.time() - start_time
    
    # Schedule next check
    delay_ms = int(self.scan_delay * 1000)
    self.root.after(delay_ms, self.check_for_death)
```
