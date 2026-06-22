# ThaiAn Hub - SRT Automatic Typewriter Bot

## 🛠️ How It Works (Technical Mechanism)

The script automates synchronized lyric typing by executing the following pipeline:

1. **Path Resolving:** It automatically locates the `demo.srt` file in the same directory as the script using `os.path.dirname(os.path.abspath(__file__))`, preventing terminal directory mismatch errors.
2. **SRT Parsing:** It extracts the exact start time, end time, and lyric text from each subtitle block, then converts the `HH:MM:SS,mmm` timestamp into raw seconds.
3. **Timeline Synchronization:** The bot calculates the elapsed time since the script started. It pauses (`time.sleep`) until the exact millisecond the vocalist begins singing the line.
4. **Dynamic Typing Speed Control:** Instead of using fixed delays, the bot calculates a customized interval for each phrase:
   $$\text{Interval Per Character} = \frac{\text{End Time} - \text{Start Time}}{\text{Total Characters}} \times 0.90$$
   *(The $0.90$ coefficient is a safety buffer applied to compensate for Operating System input lag).*
5. **Continuous Simulation:** It invokes `pyautogui.typewrite(text, interval=...)` to push the entire line stream directly into the OS keyboard buffer. This forces a smooth, continuous human-like typewriter effect with perfect word spacing.

---

## 🎯 How to Use (Step-by-Step Guide)

### 1. Preparation
* Ensure you have Python installed on your computer.
* Open your terminal and install the required library:
        pip install pyautogui
### 2. File Setup
Place both files inside the exact same directory:

 -lyric_bot.py (The main script)

 -demo.srt (You can find your .srt file by going to Google and typing: [your song title] srt, must be named exactly 'namefile.srt')

### 3. Execution
* 1.Run the script via your terminal:

        python lyric_bot.py

* 2.You will see a 5-second countdown on the console.

* 3.Immediately click your mouse cursor inside the text box of your target application (e.g., Notepad, CapCut Text Box, Adobe Premiere, Word).

* 4.Keep the target window focused until the bot finishes typing the entire playlist.
