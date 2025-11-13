# Hand Drawing Application 🎨✋

A powerful, gesture-based drawing application featuring real-time hand tracking, multiple drawing tools, and intuitive gesture controls.

> 🎨 Built by **Plasma**

## 📚 Table of Contents

- [About](#hand-drawing-application-)
- [Features](#-features)
- [Installation & Setup](#-installation-setup--execution)
- [Technical Details](#-technical-details)
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

## 🚀 Installation, Setup & Execution

### Prerequisites
**Python 3.12 Installation:**
- Download and install **Python 3.12** from [python.org](https://www.python.org/downloads/)
- **CRITICAL**: During installation, check **"Add Python to PATH"**
- **IMPORTANT**: Disable Windows path length limits when prompted

### Step-by-Step Setup

1. **Create Project Folder**
   ```bash
   # Create a dedicated folder for your drawing project
   mkdir hand_drawing_app
   ```

2. **Navigate to Your Project Folder**
   ```bash
   # Go into the folder you just created
   cd hand_drawing_app
   ```

3. **Place Your Files**
   - Copy `index.py` and `README.md` into the `hand_drawing_app` folder
   - Your folder structure should look like:
     ```
     hand_drawing_app/
     ├── index.py
     └── README.md
     ```

4. **Set Up Virtual Environment**
   ```bash
   # Create virtual environment (run this inside hand_drawing_app folder)
   py -3.12 -m venv hand_drawing_env

   # Activate the environment
   hand_drawing_env\Scripts\activate
   
   # Your command prompt should now show (hand_drawing_env)
   ```

5. **Install Dependencies**
   ```bash
   # Install required packages (with activated environment)
   pip install mediapipe opencv-python numpy
   ```

### 🎯 Execution (Every Time You Want to Run the App)

**Important: You must activate the environment every time you open a new terminal session**

```bash
# 1. Navigate to your project folder
cd hand_drawing_app

# 2. Activate the virtual environment
hand_drawing_env\Scripts\activate

# 3. Run the application (you should see (hand_drawing_env) in your prompt)
python index.py
```

### 📁 Directory Management Tips

**If you need to find your folder later:**
```bash
# Navigate to your hand_drawing_app folder
cd path\to\hand_drawing_app

# Example if it's on your Desktop:
cd Desktop\hand_drawing_app

# Example if it's in Documents:
cd Documents\hand_drawing_app
```

**To check your current directory:**
```bash
# See what folder you're currently in
dir  # Windows
```

### 🔄 Quick Start (For Future Sessions)

When you want to run the app again later:

1. Open Command Prompt
2. ```bash
   cd hand_drawing_app
   hand_drawing_env\Scripts\activate
   python index.py
   ```

### ✅ Verification Checklist
- [ ] Python 3.12 installed with PATH enabled
- [ ] Project folder created (`hand_drawing_app`)
- [ ] Used `cd hand_drawing_app` to enter the folder
- [ ] Files placed in the project folder
- [ ] Virtual environment created and activated
- [ ] All packages installed successfully
- [ ] **Remember to activate environment every time**
- [ ] Webcam connected and accessible

## 🛠️ Technical Details

### Architecture Overview
- **Computer Vision**: MediaPipe Hands for 21-point hand landmark detection
- **Real-time Processing**: OpenCV for video capture and processing at 60 FPS
- **Gesture Recognition**: Custom pinch detection algorithms with confidence scoring
- **Drawing Engine**: Custom-built with NumPy for performance
- **Coordinate System**: Real-time mapping of hand coordinates to canvas coordinates

### Core Components
- **Hand Landmark Detection**: 21 points per hand with 3D spatial coordinates
- **Pinch Gesture Recognition**: Euclidean distance-based detection with thresholding
- **Motion Smoothing**: Exponential moving average for stable cursor movement
- **Tool System**: Modular design for easy extension of drawing tools
- **Canvas Management**: Layered drawing system with undo/redo functionality

### Performance Specifications
- **Frame Rate**: 60 FPS processing target
- **Latency**: <100ms end-to-end gesture recognition
- **Resolution**: 1280x720 webcam input, 1920x1080 canvas output
- **Memory Usage**: Optimized for real-time performance

## 🔧 How It Works

- Uses your webcam to track hand movements in real-time
- Detects specific pinch gestures for tool selection and drawing
- Left hand: selects tools and adjusts settings via different finger-thumb pinches
- Right hand: performs drawing/erasing actions and changes colors
- Processes video at 60 FPS for smooth, responsive drawing
- Uses motion prediction for fluid line drawing

## 🧪 How To Use

1. Set up the virtual environment and install dependencies as shown above
2. **Remember to activate the environment every time** you run the app
3. Run the script: `python index.py`
4. Allow webcam access when prompted
5. Position your hands in view of the camera
6. Use gesture controls to start drawing
7. To exit, press **Q** or close the application window

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
- `hand_drawing_env/` → Virtual environment folder (created during setup)

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
- Verify virtual environment is activated (you should see `(hand_drawing_env)` in prompt)
- Check webcam is not used by other applications
- Ensure good lighting for hand tracking
- **Remember to activate environment every time**: `hand_drawing_env\Scripts\activate`

**If activation fails:**
```bash
# Try this instead:
.\hand_drawing_env\Scripts\activate
```

**If you forget to activate the environment:**
- You'll get import errors for mediapipe/opencv
- Simply activate it and try again: `hand_drawing_env\Scripts\activate`

**If "cd" doesn't work:**
- Make sure the folder exists and you're using the correct path
- Use File Explorer to navigate to the folder, then right-click and "Open in Terminal"

**To deactivate environment when done:**
```bash
deactivate
```

## ❓ FAQ

#### 🤔 Why Python 3.12 specifically?
MediaPipe has best compatibility with Python 3.12. Newer versions (3.13+) may have compatibility issues.

#### 💻 What if `py -3.12` doesn't work?
Make sure Python 3.12 is installed and in your PATH. You can also try:
```bash
python3.12 -m venv hand_drawing_env
```

#### 🔄 Do I need to set up the environment every time?
No! You only set up the virtual environment once. But you **must activate it every time** you run the app using `hand_drawing_env\Scripts\activate`

#### 📸 Is my webcam data secure?
Yes! All processing happens locally on your computer. No images or data are sent over the internet.

#### 🎮 Why aren't my gestures being detected?
- Check lighting conditions
- Ensure your hand is fully visible
- Try different distances from the camera
- Make deliberate, clear gestures

#### 💾 Where are my drawings saved?
Drawings are automatically saved in the `saved_drawings/` folder with timestamps.

#### 🖥️ What are the system requirements?
- Minimum: Dual-core processor, 4GB RAM, 720p webcam
- Recommended: Quad-core processor, 8GB RAM, 1080p webcam

#### 🎨 Can I customize the brush colors?
Yes! Use the color change gesture or keyboard shortcut to cycle through predefined colors.

## 💬 Need Help?

Join our **Discord Support Server**:  
👉 [![Hand Drawing App](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/https://discord.gg/Bkp4AT3UAv)

We're happy to help with:

- 🐛 Bug reports and technical issues  
- 💡 Feature suggestions and improvements
- 🙋 General setup and usage support
- 🎨 Drawing tips and techniques

**Follow me online:**  
🔗 GitHub – [![Plasma](https://img.shields.io/badge/GitHub-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ishaansucksatlife)

📱 Discord - [![Hand Drawing App](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/https://discord.gg/Bkp4AT3UAv)

## 📄 License

**GNU General Public License v3.0**

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for the full text.

### Key Protections:
- 🚫 **No proprietary use** - Derivative works must be open source
- 📝 **Attribution required** - Must preserve copyright notices
- 🛡️ **Patent protection** - Prevents patent claims on this work
- 🔓 **Source access** - Must provide source code for distributed versions

### What this means:
- You can use, modify, and share this code
- You **cannot** use it in closed-source commercial products
- You **must** keep all copyright notices and license information
- Any modifications must be released under GPL v3.0

For complete terms and conditions, see the [LICENSE](LICENSE) file.

## 🤝 Contributing

We welcome contributions! Please feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 🏷 Tags

`computer-vision` `hand-tracking` `mediapipe` `opencv` `drawing-app` `gesture-control` `python` `real-time` `creative-tools` `open-source` `digital-art` `ai` `human-computer-interaction`

---
