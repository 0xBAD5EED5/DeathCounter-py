#!/usr/bin/env python3
"""
Death Counter - Real-time OCR-based death counter for FromSoftware games

This script monitors your screen using OCR to detect death messages
from FromSoftware games (Dark Souls, Elden Ring, Sekiro, Bloodborne, etc.)
and automatically counts deaths.

Supported death messages:
- French: "VOUS ÊTES MORT" (Dark Souls), "VOUS AVEZ PÉRI" (Elden Ring)
- English: "YOU DIED"

Author: [0xBAD5EED5]
License: MIT
"""

import time
from PIL import ImageGrab, ImageEnhance, ImageFilter
import easyocr
import unicodedata
import numpy as np
import os
import json


# --- Screen and capture zone configuration ---
primary_screen = {'origin': (0, 0), 'resolution': (1920, 1080)}
secondary_screen = {'origin': (1920, 0), 'resolution': (1920, 1080)}
# OCR capture zone dimensions
capture_zone_width = 1500
capture_zone_height = 250
# Verbose mode (True = displays all recognized text, False = silent)
verbose_mode = False
# Debug mode (True = saves screenshots when death detected, False = normal)
debug_mode = False
scan_delay_seconds = 1

def preprocess_image(image):
    """Enhance image for better OCR recognition"""
    try:
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Increase contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # Increase sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.5)
        
        # Apply filter to reduce noise
        image = image.filter(ImageFilter.MedianFilter())
        
        return image
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        return image

# --- Function to get center zone coordinates ---
def get_centered_capture_zone(screen):
    """Calculate centered capture zone coordinates for a given screen"""
    origin_x, origin_y = screen['origin']
    screen_width, screen_height = screen['resolution']
    left = origin_x + (screen_width - capture_zone_width) // 2
    top = origin_y + (screen_height - capture_zone_height) // 2
    right = left + capture_zone_width
    bottom = top + capture_zone_height
    return (left, top, right, bottom)

capture_zone = get_centered_capture_zone(primary_screen) 

# --- OCR & Accent removal ---
ocr_reader = easyocr.Reader(['fr', 'en'])

def remove_text_accents(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

# --- Death detection ---
def is_death_message_detected(ocr_results):
    """Check if FromSoftware death message is present in OCR results"""
    # FromSoftware games death messages
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
        "YOU  DIED", "YOUDIED", "YOU DIEU"  # Common OCR mistakes
    ]
    
    for detection in ocr_results:
        # Check minimum confidence
        if detection[2] < 0.4:  # Slightly higher threshold for better accuracy
            continue
            
        detected_text = remove_text_accents(detection[1].upper()).strip()
        # Remove extra spaces
        detected_text = ' '.join(detected_text.split())
        
        # Exact verification
        for death_message in death_messages:
            if death_message in detected_text:
                if verbose_mode:
                    print(f"💀 Found death message: '{death_message}' in '{detected_text}'")
                return True
                
        # Approximate verification for OCR errors (more lenient for FromSoftware messages)
        primary_death_messages = ["VOUS ETES MORT", "VOUS AVEZ PERI", "YOU DIED"]
        for death_message in primary_death_messages:
            text_similarity = calculate_text_similarity(detected_text, death_message)
            if text_similarity > 0.75:  # Lower threshold for these specific messages
                if verbose_mode:
                    print(f"💀 Found similar death message: '{detected_text}' matches '{death_message}' ({text_similarity:.2f})")
                return True
    
    return False

def calculate_text_similarity(text1, text2):
    """Calculate simple similarity between two texts"""
    if not text1 or not text2:
        return 0
    
    # Number of common characters
    common_characters = sum(1 for a, b in zip(text1, text2) if a == b)
    max_length = max(len(text1), len(text2))
    
    if max_length == 0:
        return 0
    
    return common_characters / max_length

# --- Death counter functions ---
def load_death_counter():
    """Load counter from JSON file"""
    try:
        if os.path.exists('death_counter.json'):
            with open('death_counter.json', 'r') as f:
                data = json.load(f)
                return data.get('counter', 0)
    except Exception as e:
        print(f"Error loading counter: {e}")
    return 0

def save_death_counter(death_count):
    """Save counter to JSON file"""
    try:
        with open('death_counter.json', 'w') as f:
            json.dump({'counter': death_count}, f)
    except Exception as e:
        print(f"Error saving counter: {e}")

death_counter = load_death_counter()
death_already_detected = False

if death_counter > 0:
    print(f"Counter loaded: {death_counter} previous deaths")
print("Starting death counter... Ctrl+C to stop.")

loop_iteration_counter = 0  # Loop counter for status display

try:
    while True:
        try:
            # Capture screen
            screen_capture = ImageGrab.grab(bbox=capture_zone)
            
            # Preprocess image to improve OCR
            enhanced_image = preprocess_image(screen_capture)
            
            # Perform OCR on preprocessed image
            ocr_result = ocr_reader.readtext(np.array(enhanced_image))
            
            # Also try with original image if nothing found
            if not ocr_result or len(ocr_result) == 0:
                ocr_result = ocr_reader.readtext(np.array(screen_capture))

            if verbose_mode:
                for detection in ocr_result:
                    print(f"Recognized text: '{detection[1]}' (confidence {detection[2]:.2f})")

            if is_death_message_detected(ocr_result):
                if not death_already_detected:
                    death_counter += 1
                    save_death_counter(death_counter)  # Immediate save
                    print(f"💀 Death detected! Counter: {death_counter}")
                    
                    # Save screenshot in debug mode
                    if debug_mode:
                        timestamp = int(time.time())
                        screen_capture.save(f"death_screenshot_{timestamp}.png")
                        enhanced_image.save(f"death_processed_{timestamp}.png")
                        print(f"📸 Screenshots saved: death_screenshot_{timestamp}.png")
                    
                    death_already_detected = True
            else:
                death_already_detected = False

            # Status display every 10 loops
            if loop_iteration_counter % 10 == 0:
                print(f"🎮 Active monitoring... Current deaths: {death_counter}")

        except Exception as e:
            print(f"Error during capture/analysis: {e}")
            
        # Reduce scan frequency when nothing happens
        if not is_death_message_detected(ocr_result if 'ocr_result' in locals() else []):
            time.sleep(scan_delay_seconds)  # Slower when no death
        else:
            time.sleep(0.5)  # Faster during deaths

        loop_iteration_counter += 1  # Increment loop counter

except KeyboardInterrupt:
    print(f"\n🛑 Program stopped. Total deaths: {death_counter}")
except Exception as e:
    print(f"Critical error: {e}")
