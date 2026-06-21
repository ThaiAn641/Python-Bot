
## ⚙️ How It Works

The engine processes video data into a high-definition color text matrix through the following internal pipeline:

1. **Micro-Font Generation:** Upon startup, the script pre-renders characters from the ASCII palette into tiny `3x5` pixel texture masks using OpenCV's font engine.
2. **Frame Scaling:** Every incoming video frame is scaled down to match the specified grid columns (`target_width`), preserving the original video's aspect ratio.
3. **Extreme Saturation Boost:** The frame colors are converted to HSV space where saturation is multiplied by `2.0` (200% boost). This makes the final character grid look vivid, neon-bright, and cinematic.
4. **Vectorized NumPy Masking:** Instead of using slow CPU loops to draw text, the bot utilizes high-speed NumPy indexing. It maps the brightness of the grayscale frame directly onto the pre-rendered character masks and overlays the boosted color values simultaneously. This speeds up the process by over 50x.
5. **GUI Canvas Rendering:** The finalized character image grid is flashed directly onto an independent native OpenCV graphics window, running smoothly at real-time video FPS without any screen-flickering issues.

---

## 🛠️ How To Use

### 1. Install Dependencies
Make sure you have **Python** installed. Open your terminal (Command Prompt / VS Code Terminal) and install the required modules:
         
         pip install opencv-python numpy

### 2. File Setup
Place your target .mp4 video file into the same folder/directory as your video_ASCII.py script.

Rename your video file to bad_apple.mp4 (or change the filename directly inside the script at the video_filename variable).

### 3. Execution
To run the project safely and avoid extension bugs (like Code Runner executing temporary selections), run the script directly from your terminal console:

         python "video_ASCII.py"

### 4. Adjusting Resolution
You can tweak the matrix sharpness at the bottom of the script by changing the value of the target_width variable:
# Open video_ASCII.py and edit this slider variable:
target_width = 420  # Options: 300 (Balanced) | 420 (Ultra Sharp) | 500+ (Hardware Killer)
Tip: Once the playback window opens, maximize it to full screen. Because the font is set to a micro-size (3x5), expanding the window blends the colors beautifully.

### 5. Hotkeys & Controls
While the ASCII graphic window is active on your screen, you can close the bot instantly by pressing:

The ESC key on your keyboard.

Or the q key (lowercase).
