# Hand Drawing Application 🎨✋

A powerful, gesture-based drawing application featuring real-time hand tracking, multiple drawing tools, and intuitive gesture controls.

> 🎨 Built by **Your Name**

## 📚 Table of Contents

- [About](#hand-drawing-application-)
- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [How It Works](#-how-it-works)
- [How To Use](#-how-to-use)
- [Gesture Controls](#gesture-controls)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Supported Tools](#-supported-tools)
- [Included Files](#-included-files)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Need Help?](#-need-help)

---

## 🔥 Features

🎨 **Multi-Tool Drawing Interface**  
Brush, spray, and fill tools with customizable sizes and colors.

✋ **Real-Time Hand Tracking**  
Advanced MediaPipe hand landmark detection with 21 points per hand.

⚙️ **Rich Gesture Configuration**  
• Left-hand tool selection • Right-hand drawing actions • Custom brush sizes • Multiple color options

💥 **Dual-Hand Coordination**  
Left hand controls tools, right hand performs drawing actions simultaneously.

🛡️ **Smart Gesture Recognition**  
Advanced pinch detection with confidence scoring and motion smoothing.

🛑 **Instant Tool Switching**  
Change tools, colors, and settings with simple hand gestures.

💡 **Real-Time Performance Feedback**  
Live FPS monitoring, gesture confidence scores, and status indicators.

🚀 **Multiple Drawing Modes**  
Choose between brush, spray can, and fill bucket tools.

👾 **Customizable Interface**  
Toggle UI elements and adjust settings on the fly.

## 📦 Requirements

- **Python 3.12** (required for MediaPipe compatibility)
- Webcam (built-in or external)
- The following Python packages: `opencv-python`, `numpy`, `mediapipe`

## 🚀 Installation

```bash
# Create new virtual environment with Python 3.12
py -3.12 -m venv hand_drawing_env

# Activate it
hand_drawing_env\Scripts\activate

# Install all required packages
pip install mediapipe opencv-python numpy

# Run your application
python index.py
```

## 🔧 How It Works

- Uses your webcam to track hand movements in real-time
- Detects specific pinch gestures for tool selection and drawing
- Left hand: selects tools and adjusts settings via different finger-thumb pinches
- Right hand: performs drawing/erasing actions and changes colors
- Processes video at 60 FPS for smooth, responsive drawing
- Uses motion prediction for fluid line drawing

## 🧪 How To Use

1. Set up the virtual environment and install dependencies as shown above
2. Run the script: `python index.py`
3. Allow webcam access when prompted
4. Position your hands in view of the camera
5. Use gesture controls to start drawing
6. To exit, press **Q** or close the application window

## 👆 Gesture Controls

### Left Hand (Tool Selection)
- **Index + Thumb** → Brush tool
- **Middle + Thumb** → Spray tool  
- **Ring + Thumb** → Change brush size (hold 1 second)
- **Pinky + Thumb** → Fill tool

### Right Hand (Drawing Actions)  
- **Index + Thumb** → Draw with selected tool
- **Middle + Thumb** → Erase
- **Pinky + Thumb** → Change color

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Q** | Quit application |
| **C** | Clear canvas |
| **S** | Save drawing |
| **Z** | Undo |
| **Y** | Redo |
| **+/-** | Adjust brush size |
| **[/]** | Adjust eraser size |
| **T** | Cycle through tools |
| **N** | Change color |
| **Space** | Toggle interface display |

## 🧩 Supported Tools

• 🖌️ **Brush Tool** - Smooth, anti-aliased drawing with variable sizes  
• 🎯 **Spray Tool** - Spray paint effect with customizable density  
• 🎨 **Fill Tool** - Flood fill with smart color tolerance  
• 🧽 **Eraser** - Multiple sizes for precise editing  

## 📂 Included Files

- `index.py` → The main application source code  
- `README.md` → This help file with setup instructions  
- `saved_drawings/` → Auto-created folder for your artwork

## 🔧 Troubleshooting

### If Installation Fails:

**Ensure you're using Python 3.12** (required for MediaPipe):

```bash
# Check your Python version
py -3.12 --version

# If Python 3.12 is not installed, download it first from python.org
```

**Update pip first:**
```bash
python -m pip install --upgrade pip
```

**Common Issues:**
- Ensure Python 3.12 is installed and available as `py -3.12`
- Verify virtual environment is activated
- Check webcam is not used by other applications
- Ensure good lighting for hand tracking

## ❓ FAQ

#### 🤔 Why Python 3.12 specifically?
MediaPipe has best compatibility with Python 3.12. Newer versions (3.13+) may have compatibility issues.

#### 💻 What if `py -3.12` doesn't work?
Make sure Python 3.12 is installed and in your PATH. You can also try:
```bash
python3.12 -m venv hand_drawing_env
```

#### 📸 Is my webcam data secure?
Yes! All processing happens locally on your computer. No images or data are sent over the internet.

#### 🎮 Why aren't my gestures being detected?
- Check lighting conditions
- Ensure your hand is fully visible
- Try different distances from the camera
- Make deliberate, clear gestures

#### 💾 Where are my drawings saved?
Drawings are automatically saved in the `saved_drawings/` folder with timestamps.

## 💬 Need Help?

Join our **Discord Support Server**:  
👉 [![Hand Drawing App](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/your-invite-link)

We're happy to help with:

- 🐛 Bug reports and technical issues  
- 💡 Feature suggestions and improvements
- 🙋 General setup and usage support
- 🎨 Drawing tips and techniques


**Follow me online:**  
🔗 GitHub – [![YourUsername](https://img.shields.io/badge/GitHub-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/yourusername)

📱 Discord - [![Hand Drawing App](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/your-invite-link)

## 🏷 Tags

`computer-vision` `hand-tracking` `mediapipe` `opencv` `drawing-app` `gesture-control` `python` `real-time` `creative-tools` `open-source` `digital-art` `ai` `human-computer-interaction`
