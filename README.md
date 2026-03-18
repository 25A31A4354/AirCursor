# AirCursor

Control your computer's cursor using hand gestures in the air! This project uses OpenCV, MediaPipe, and PyAutoGUI to track your hand movements through your webcam and translate them into mouse actions.

## Features

- **Cursor Movement**: Move your index finger to control the cursor.
- **Left Click**: Pinch your index finger and thumb together.
- **Right Click**: Pinch your middle finger and thumb together.
- **Scroll Up/Down**: Move your index and middle fingers together up or down.
- **Next/Previous Slide**: Specific gestures using middle, ring, and pinky fingers.

## Requirements

- Python 3.9+
- A working webcam

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/AirCursor.git
cd AirCursor
```

2. Create a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:

```bash
python aircursor_final.py
```

A camera preview window will appear in the bottom right corner of your screen. Press the `ESC` key while the window is focused to close the application.
