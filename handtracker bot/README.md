
## ⚙️ Technical Specifications
* **Multi-Jointed Skeleton:** Triple-bone replication (x3 joint density) creates a high-fidelity Android skeleton structure.
* **Ultra-HD Core:** Forces high-definition camera resolution combined with a **Sharpening Kernel** to eliminate sensor noise and blur.
* **Smart Gesture Trigger:** Features a "Middle Finger Trigger" that allows real-time rendering of custom user-defined assets (Custom Asset Overlay).
* **Hybrid Scan:** Simultaneous dual-hand and full-body tracking, with facial node suppression for clean aesthetic output.

## 🚀 How it Works
1. **Initialization:** The system activates dual detectors (Pose & Hand) to map a 33-point body skeleton and a 21-point hand skeleton simultaneously.
2. **Image Processing:** Frames are sharpened via a convolution filter and contrast-boosted to highlight the Neon Glow skeleton layer.
3. **Robotic Logic:** The engine performs coordinate interpolation (at 1/3 and 2/3 of the bone length) to inject secondary mechanical joints, creating a "cybernetic" look.
4. **Trigger:** Upon detecting the middle finger gesture, the system overlays `ngongiua.png` at the coordinates of the 12th landmark (middle finger tip).

## ⚡ User Guide

### 1. Preparation
* Ensure required libraries are installed: `pip install cvzone mediapipe opencv-python`.

### 2. Execution
Open your Terminal/Command Prompt in the project folder and run:

         python Handtracker_bot.py

### 3. Controls
Detection: Stand back for full-body tracking. Move hands closer for precision finger tracking.

Interaction: Raise your middle finger to trigger the custom asset overlay.

Shutdown: Press q or ESC to terminate the system
