#!/bin/bash
# Launch script for Death Counter GUI

echo "Starting Death Counter GUI..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Launch the application
python3 death_counter_gui.py
