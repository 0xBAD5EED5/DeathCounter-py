#!/usr/bin/env python3
"""
Death Counter GUI - Real-time OCR-based death counter for FromSoftware games

This script monitors your screen using OCR to detect death messages
from FromSoftware games (Dark Souls, Elden Ring, Sekiro, Bloodborne, etc.)
and automatically counts deaths.

Features:
- Auto-detection of screen resolutions
- Cross-platform GUI (Linux/Mac/Windows)
- Flexible configuration
- Real-time monitoring

Author: [0xBAD5EED5]
License: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from PIL import ImageGrab, ImageEnhance, ImageFilter, Image
import easyocr
import unicodedata
import numpy as np
import os
import json
import platform
import sys

class DeathCounterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Death Counter - FromSoftware Games")
        self.root.geometry("800x600")
        
        # Variables
        self.death_counter = tk.IntVar(value=0)
        self.is_monitoring = False
        self.monitoring_thread = None
        self.death_already_detected = False
        
        # Configuration
        self.config = {
            'capture_zone_width': 1500,
            'capture_zone_height': 250,
            'verbose_mode': False,
            'debug_mode': False,
            'scan_delay': 1.0,
            'confidence_threshold': 0.4,
            'selected_screen': 0
        }
        
        # Initialize OCR reader
        self.ocr_reader = None
        self.initialize_ocr()
        
        # Detect available screens
        self.available_screens = self.detect_screens()
        
        # Load death counter from file
        self.load_death_counter()
        
        # Create GUI interface
        self.create_gui()
        
        # Load saved configuration
        self.load_configuration()

    def detect_screens(self):
        """Detect all available screens and their resolutions"""
        detected_screens = []
        
        try:
            # Get total screen dimensions
            total_screen_width = self.root.winfo_screenwidth()
            total_screen_height = self.root.winfo_screenheight()
            
            # Try to detect multiple monitors (basic approach)
            # This works for most setups but may need refinement for complex multi-monitor setups
            
            # Primary screen (always exists)
            detected_screens.append({
                'name': 'Primary Screen',
                'origin': (0, 0),
                'resolution': (total_screen_width, total_screen_height),
                'description': f'Primary ({total_screen_width}x{total_screen_height})'
            })
            
            # Try to detect if we have a multi-monitor setup
            # This is a simplified approach - in reality, we'd need platform-specific code
            # for more accurate detection
            if total_screen_width > 2560:  # Likely dual monitor setup
                # Assume common dual monitor setup
                single_screen_width = total_screen_width // 2
                detected_screens = [
                    {
                        'name': 'Left Monitor',
                        'origin': (0, 0),
                        'resolution': (single_screen_width, total_screen_height),
                        'description': f'Left ({single_screen_width}x{total_screen_height})'
                    },
                    {
                        'name': 'Right Monitor', 
                        'origin': (single_screen_width, 0),
                        'resolution': (single_screen_width, total_screen_height),
                        'description': f'Right ({single_screen_width}x{total_screen_height})'
                    }
                ]
            
        except Exception as e:
            print(f"Error detecting screens: {e}")
            # Fallback to common resolutions
            detected_screens = [
                {
                    'name': 'Default Screen',
                    'origin': (0, 0), 
                    'resolution': (1920, 1080),
                    'description': 'Default (1920x1080)'
                }
            ]
        
        return detected_screens

    def initialize_ocr(self):
        """Initialize EasyOCR reader"""
        try:
            self.ocr_reader = easyocr.Reader(['fr', 'en'])
        except Exception as e:
            messagebox.showerror("Error", f"Unable to initialize EasyOCR: {e}")
            sys.exit(1)

    def create_gui(self):
        """Create the main GUI interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Counter display
        counter_frame = ttk.LabelFrame(main_frame, text="Death Counter", padding="10")
        counter_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(counter_frame, text="Current Deaths:", font=("Arial", 12)).grid(row=0, column=0, padx=(0, 10))
        counter_label = ttk.Label(counter_frame, textvariable=self.death_counter, font=("Arial", 16, "bold"))
        counter_label.grid(row=0, column=1)
        
        ttk.Button(counter_frame, text="Reset", command=self.reset_death_counter).grid(row=0, column=2, padx=(20, 0))
        
        # Configuration frame
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Screen selection
        ttk.Label(config_frame, text="Screen:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.selected_screen_var = tk.StringVar()
        screen_combo = ttk.Combobox(config_frame, textvariable=self.selected_screen_var, state="readonly")
        screen_combo['values'] = [screen['description'] for screen in self.available_screens]
        screen_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        screen_combo.current(0)
        
        # Zone dimensions
        ttk.Label(config_frame, text="Zone Width:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.capture_width_var = tk.IntVar(value=self.config['capture_zone_width'])
        width_spinbox = ttk.Spinbox(config_frame, from_=500, to=3000, textvariable=self.capture_width_var, width=10)
        width_spinbox.grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        ttk.Label(config_frame, text="Zone Height:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.capture_height_var = tk.IntVar(value=self.config['capture_zone_height'])
        height_spinbox = ttk.Spinbox(config_frame, from_=100, to=800, textvariable=self.capture_height_var, width=10)
        height_spinbox.grid(row=2, column=1, sticky=tk.W, pady=(5, 0))
        
        # Scan delay
        ttk.Label(config_frame, text="Scan Delay (s):").grid(row=3, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.scan_delay_var = tk.DoubleVar(value=self.config['scan_delay'])
        delay_spinbox = ttk.Spinbox(config_frame, from_=0.1, to=5.0, increment=0.1, textvariable=self.scan_delay_var, width=10)
        delay_spinbox.grid(row=3, column=1, sticky=tk.W, pady=(5, 0))
        
        # Options checkboxes
        options_frame = ttk.Frame(config_frame)
        options_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.verbose_mode_var = tk.BooleanVar(value=self.config['verbose_mode'])
        ttk.Checkbutton(options_frame, text="Verbose Mode", variable=self.verbose_mode_var).grid(row=0, column=0, sticky=tk.W)
        
        self.debug_mode_var = tk.BooleanVar(value=self.config['debug_mode'])
        ttk.Checkbutton(options_frame, text="Debug Mode", variable=self.debug_mode_var).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        self.start_monitoring_button = ttk.Button(control_frame, text="Start", command=self.start_death_monitoring)
        self.start_monitoring_button.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_monitoring_button = ttk.Button(control_frame, text="Stop", command=self.stop_death_monitoring, state="disabled")
        self.stop_monitoring_button.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(control_frame, text="Test Zone", command=self.test_capture_zone).grid(row=0, column=2, padx=(0, 10))
        
        # Status and log
        status_frame = ttk.LabelFrame(main_frame, text="Status and Logs", padding="10")
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Status
        self.monitoring_status_var = tk.StringVar(value="Ready")
        ttk.Label(status_frame, text="Status:").grid(row=0, column=0, sticky=tk.W)
        status_label = ttk.Label(status_frame, textvariable=self.monitoring_status_var, foreground="green")
        status_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Log text area
        log_frame = ttk.Frame(status_frame)
        log_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.log_text_widget = tk.Text(log_frame, height=15, width=70)
        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text_widget.yview)
        self.log_text_widget.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        config_frame.columnconfigure(1, weight=1)
        status_frame.columnconfigure(1, weight=1)
        status_frame.rowconfigure(1, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Menu
        self.create_menu()

    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Config", command=self.save_configuration)
        file_menu.add_command(label="Load Config", command=self.load_configuration)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_window_closing)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about_dialog)

    def add_log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Thread-safe GUI update
        self.root.after(0, self._update_log_widget, log_entry)

    def _update_log_widget(self, message):
        """Update log text widget (GUI thread)"""
        self.log_text_widget.insert(tk.END, message)
        self.log_text_widget.see(tk.END)

    def get_centered_capture_zone(self, screen):
        """Calculate centered capture zone coordinates for a given screen"""
        origin_x, origin_y = screen['origin']
        screen_width, screen_height = screen['resolution']
        zone_width = self.capture_width_var.get()
        zone_height = self.capture_height_var.get()
        
        left = origin_x + (screen_width - zone_width) // 2
        top = origin_y + (screen_height - zone_height) // 2
        right = left + zone_width
        bottom = top + zone_height
        return (left, top, right, bottom)

    def enhance_image_for_ocr(self, image):
        """Enhance image for better OCR recognition"""
        try:
            if image.mode != 'L':
                image = image.convert('L')
            
            contrast_enhancer = ImageEnhance.Contrast(image)
            image = contrast_enhancer.enhance(2.0)
            
            sharpness_enhancer = ImageEnhance.Sharpness(image)
            image = sharpness_enhancer.enhance(1.5)
            
            image = image.filter(ImageFilter.MedianFilter())
            
            return image
        except Exception as e:
            self.add_log_message(f"Error preprocessing image: {e}")
            return image

    def remove_text_accents(self, text):
        """Remove accents from text"""
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )

    def is_death_message_detected(self, ocr_results):
        """Check if FromSoftware death message is present in OCR results"""
        death_messages = [
            # French - Dark Souls series
            "VOUS ETES MORT", "VOUS ÊTES MORT",
            # French - Elden Ring
            "VOUS AVEZ PERI", "VOUS AVEZ PÉRI",
            # English - All games
            "YOU DIED",
            # Possible OCR variations (missing accents, spacing issues)
            "VOUS ETE MORT", "VOUS ETÉS MORT", "VOUS ETES  MORT",
            "VOUS AVEZ PERI", "VOUS AVEZ  PERI", "VOUSAVEZPERI",
            "YOU  DIED", "YOUDIED", "YOU DIEU"
        ]
        
        for detection in ocr_results:
            if detection[2] < 0.4:
                continue
                
            detected_text = self.remove_text_accents(detection[1].upper()).strip()
            detected_text = ' '.join(detected_text.split())
            
            for death_message in death_messages:
                if death_message in detected_text:
                    if self.verbose_mode_var.get():
                        self.add_log_message(f"💀 Death message found: '{death_message}' in '{detected_text}'")
                    return True
                    
            # Similarity check
            primary_death_messages = ["VOUS ETES MORT", "VOUS AVEZ PERI", "YOU DIED"]
            for death_message in primary_death_messages:
                text_similarity = self.calculate_text_similarity(detected_text, death_message)
                if text_similarity > 0.75:
                    if self.verbose_mode_var.get():
                        self.add_log_message(f"💀 Similar death message: '{detected_text}' matches '{death_message}' ({text_similarity:.2f})")
                    return True
        
        return False

    def calculate_text_similarity(self, text1, text2):
        """Calculate simple similarity between two texts"""
        if not text1 or not text2:
            return 0
        
        common_characters = sum(1 for a, b in zip(text1, text2) if a == b)
        max_length = max(len(text1), len(text2))
        
        return common_characters / max_length if max_length > 0 else 0

    def death_monitoring_loop(self):
        """Main monitoring loop (runs in separate thread)"""
        selected_screen_description = self.selected_screen_var.get()
        screen_index = next((i for i, screen in enumerate(self.available_screens) 
                          if screen['description'] == selected_screen_description), 0)
        
        selected_screen = self.available_screens[screen_index]
        capture_zone = self.get_centered_capture_zone(selected_screen)
        
        self.add_log_message(f"Starting monitoring on screen: {selected_screen['description']}")
        self.add_log_message(f"Capture zone: {capture_zone}")
        
        loop_iteration_counter = 0
        
        while self.is_monitoring:
            try:
                # Capture screen
                screen_capture = ImageGrab.grab(bbox=capture_zone)
                
                # Preprocess image
                enhanced_image = self.enhance_image_for_ocr(screen_capture)
                
                # OCR
                ocr_result = self.ocr_reader.readtext(np.array(enhanced_image))
                
                if not ocr_result:
                    ocr_result = self.ocr_reader.readtext(np.array(screen_capture))

                if self.verbose_mode_var.get():
                    for detection in ocr_result:
                        self.add_log_message(f"Recognized text: '{detection[1]}' (confidence {detection[2]:.2f})")

                if self.is_death_message_detected(ocr_result):
                    if not self.death_already_detected:
                        current_death_count = self.death_counter.get() + 1
                        self.death_counter.set(current_death_count)
                        self.save_death_counter()
                        self.add_log_message(f"💀 Death detected! Counter: {current_death_count}")
                        
                        if self.debug_mode_var.get():
                            timestamp = int(time.time())
                            screen_capture.save(f"death_screenshot_{timestamp}.png")
                            enhanced_image.save(f"death_processed_{timestamp}.png")
                            self.add_log_message(f"📸 Screenshots saved: death_screenshot_{timestamp}.png")
                        
                        self.death_already_detected = True
                else:
                    self.death_already_detected = False

                # Status update every 10 loops
                if loop_iteration_counter % 10 == 0:
                    self.root.after(0, self.monitoring_status_var.set, f"Monitoring active... Deaths: {self.death_counter.get()}")

            except Exception as e:
                self.add_log_message(f"Error during capture/analysis: {e}")
                
            time.sleep(self.scan_delay_var.get())
            loop_iteration_counter += 1

    def start_death_monitoring(self):
        """Start death monitoring"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.death_already_detected = False
            
            self.start_monitoring_button.config(state="disabled")
            self.stop_monitoring_button.config(state="normal")
            
            self.monitoring_thread = threading.Thread(target=self.death_monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            
            self.monitoring_status_var.set("Monitoring in progress...")
            self.add_log_message("🎮 Monitoring started")

    def stop_death_monitoring(self):
        """Stop death monitoring"""
        if self.is_monitoring:
            self.is_monitoring = False
            
            self.start_monitoring_button.config(state="normal")
            self.stop_monitoring_button.config(state="disabled")
            
            self.monitoring_status_var.set("Stopped")
            self.add_log_message("🛑 Monitoring stopped")

    def test_capture_zone(self):
        """Test capture zone by taking a screenshot"""
        try:
            selected_screen_description = self.selected_screen_var.get()
            screen_index = next((i for i, screen in enumerate(self.available_screens) 
                              if screen['description'] == selected_screen_description), 0)
            
            selected_screen = self.available_screens[screen_index]
            capture_zone = self.get_centered_capture_zone(selected_screen)
            
            test_screenshot = ImageGrab.grab(bbox=capture_zone)
            timestamp = int(time.time())
            test_filename = f"test_capture_{timestamp}.png"
            test_screenshot.save(test_filename)
            
            self.add_log_message(f"📸 Capture zone tested and saved: {test_filename}")
            self.add_log_message(f"Zone: {capture_zone}")
            messagebox.showinfo("Test", f"Screenshot saved: {test_filename}")
            
        except Exception as e:
            self.add_log_message(f"Error testing capture: {e}")
            messagebox.showerror("Error", f"Error during test: {e}")

    def reset_death_counter(self):
        """Reset death counter"""
        if messagebox.askyesno("Reset", "Are you sure you want to reset the counter to zero?"):
            self.death_counter.set(0)
            self.save_death_counter()
            self.add_log_message("🔄 Counter reset to zero")

    def load_death_counter(self):
        """Load counter from JSON file"""
        try:
            if os.path.exists('death_counter.json'):
                with open('death_counter.json', 'r') as f:
                    data = json.load(f)
                    self.death_counter.set(data.get('counter', 0))
        except Exception as e:
            self.add_log_message(f"Error loading counter: {e}")

    def save_death_counter(self):
        """Save counter to JSON file"""
        try:
            with open('death_counter.json', 'w') as f:
                json.dump({'counter': self.death_counter.get()}, f)
        except Exception as e:
            self.add_log_message(f"Error saving counter: {e}")

    def save_configuration(self):
        """Save configuration to file"""
        config_data = {
            'capture_zone_width': self.capture_width_var.get(),
            'capture_zone_height': self.capture_height_var.get(),
            'verbose_mode': self.verbose_mode_var.get(),
            'debug_mode': self.debug_mode_var.get(),
            'scan_delay': self.scan_delay_var.get(),
            'selected_screen': self.selected_screen_var.get()
        }
        
        try:
            with open('death_counter_config.json', 'w') as f:
                json.dump(config_data, f, indent=2)
            self.add_log_message("💾 Configuration saved")
        except Exception as e:
            self.add_log_message(f"Error saving configuration: {e}")

    def load_configuration(self):
        """Load configuration from file"""
        try:
            if os.path.exists('death_counter_config.json'):
                with open('death_counter_config.json', 'r') as f:
                    config_data = json.load(f)
                    
                self.capture_width_var.set(config_data.get('capture_zone_width', 1500))
                self.capture_height_var.set(config_data.get('capture_zone_height', 250))
                self.verbose_mode_var.set(config_data.get('verbose_mode', False))
                self.debug_mode_var.set(config_data.get('debug_mode', False))
                self.scan_delay_var.set(config_data.get('scan_delay', 1.0))
                
                selected_screen_description = config_data.get('selected_screen', '')
                if selected_screen_description in [s['description'] for s in self.available_screens]:
                    self.selected_screen_var.set(selected_screen_description)
                
                self.add_log_message("📂 Configuration loaded")
        except Exception as e:
            self.add_log_message(f"Error loading configuration: {e}")

    def show_about_dialog(self):
        """Show about dialog"""
        about_text = """Death Counter GUI v1.0

Real-time death counter for FromSoftware games
(Dark Souls, Elden Ring, Sekiro, Bloodborne, etc.)

Features:
• Automatic screen detection
• Cross-platform GUI
• Flexible configuration
• Real-time monitoring
• Debug mode with screenshots

Author: [0xBAD5EED5]
License: MIT"""
        
        messagebox.showinfo("About", about_text)

    def on_window_closing(self):
        """Handle window closing"""
        if self.is_monitoring:
            self.stop_death_monitoring()
        
        self.save_configuration()
        self.root.destroy()

def main():
    """Main function"""
    root = tk.Tk()
    death_counter_app = DeathCounterGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", death_counter_app.on_window_closing)
    
    # Center window
    root.update_idletasks()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    center_x = (root.winfo_screenwidth() // 2) - (window_width // 2)
    center_y = (root.winfo_screenheight() // 2) - (window_height // 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
