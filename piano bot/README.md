
## ⚙️ How It Works

The system processes data sequentially through 4 core technical stages:

1. **MIDI Parsing & Timeline Mapping** The bot uses `mido` to scan the input `input.mid` file. It extracts the exact timestamps for `note_on` events, maps the MIDI note numbers to standard piano keys (from C4 to G5, including sharps), and pre-allocates them onto a 30-FPS video timeline grid.

2. **Visual Key Matrix Rendering** Using `opencv-python` (OpenCV), the script draws a 1280x720 Cyberpunk-themed virtual keyboard. 
   - Natural keys and accidental sharp keys (labeled with `#`) are rendered dynamically.
   - When a note event occurs, the corresponding key instantly switches to a glowing **Neon Green** state with an ivory outline.

3. **Acoustic Sound Synthesis** Instead of using algorithmic square waves, the engine searches the `piano_sounds/` directory for individual acoustic piano `.wav` samples matching the logged notes. It layers these sound waves on top of each other using the `moviepy` sound mixing core at their exact playback timestamps.

4. **Multi-Media Synchronization** Finally, `moviepy` takes the temporary silent video track and merges it with the freshly synthesized stereo sound wave, exporting a fully optimized `output.mp4` video with perfectly synchronized audio and visuals.

---

## 🚀 How to Use

Follow these simple steps to generate your piano visualizer video:

### 1. File Structure Setup
Ensure your project workspace is organized precisely as follows:
📁 piano_bot/
├── 📄 thai_an_midi_piano_pro.py  # Main engine script
├── 🎵 music.mid                 # Your input MIDI song file
└── 📁 piano_sounds/             # Folder containing single piano note samples

### 2. Generate the Perfect Piano Video
Place your target song file in the folder, rename it to music.mid, and execute the main V6 compiler:
         python thai_an_midi_piano_pro.py
Once the terminal outputs 🎉 SUCCESS!, look into your project folder to find your finished video: output.mp4!
   