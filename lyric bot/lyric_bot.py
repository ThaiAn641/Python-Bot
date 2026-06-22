import time
import re
import os
import pyautogui

# Reset pyautogui's default pause time to 0 for precise interval control
pyautogui.PAUSE = 0 

print("====================================")
print("📌 Name: ThaiAn Hub")
print("✨ Subtitle: by Zoink (ThaiAn)")
print("====================================\n")

def srt_time_to_seconds(time_str):
    """Converts SRT time format (HH:MM:SS,mmm) to total seconds (float)"""
    time_str = time_str.replace(',', '.')
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds

def parse_srt_to_playlist(file_path):
    """Parses the .srt file to extract exact start/end timestamps and lyrics"""
    if not os.path.exists(file_path):
        print(f"❌ Error: Subtitle file not found at: {file_path}")
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = content.strip().split('\n\n')
    playlist = []

    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            # Line 2 contains the timeline (e.g., 00:01:20,000 --> 00:01:23,500)
            time_match = re.match(r'(\d+:\d+:\d+,\d+)\s+-->\s+(\d+:\d+:\d+,\d+)', lines[1])
            if time_match:
                start_secs = srt_time_to_seconds(time_match.group(1))
                end_secs = srt_time_to_seconds(time_match.group(2))
                lyric_text = " ".join(lines[2:]).strip()
                
                if lyric_text:
                    playlist.append({
                        "lyric": lyric_text,
                        "start": start_secs,
                        "end": end_secs
                    })
                    
    # Sort the playlist chronologically based on start time
    playlist.sort(key=lambda x: x["start"])
    return playlist

def run_srt_pyautogui_bot(file_path):
    playlist = parse_srt_to_playlist(file_path)
    if not playlist:
        return
        
    print(f"📦 SRT file parsed successfully. Found {len(playlist)} lyric lines.")
    print("👉 You have 5 seconds to click on your target software (e.g., Notepad, CapCut)...")
    time.sleep(5)
    
    timeline_start = time.time()
    print("▶️ Start typing character by character continuously...\n")
    
    for item in playlist:
        text = item["lyric"]
        start_time = item["start"]
        end_time = item["end"]
        
        # ⏳ Synchronize starting time for the lyric line
        current_elapsed = time.time() - timeline_start
        wait_time = start_time - current_elapsed
        
        if wait_time > 0:
            time.sleep(wait_time)
            
        duration = end_time - start_time
        total_chars = len(text)
        
        if duration > 0 and total_chars > 0:
            # Calculate the precise delay between each character (including spaces)
            # Multiplied by 0.90 to compensate for OS input lag and overhead
            interval_per_char = (duration / total_chars) * 0.90
            
            # Type the entire line smoothly with the calculated speed interval
            pyautogui.typewrite(text, interval=interval_per_char)
            
            # Safety sleep to absorb any remaining time slot before the next line starts
            time.sleep(max(0, end_time - (time.time() - timeline_start)))
            
            # Press Enter to go to the next line after finishing the lyric phrase
            pyautogui.press('enter') 
            print(f"🎤 Typed: {text} ({start_time}s -> {end_time}s) | Speed: {interval_per_char:.3f}s/char")
            
    print("\n✅ All lyric lines have been processed and typed successfully!")

if __name__ == "__main__":
    # Get the absolute directory of the currently running script to prevent path mismatch errors
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_lyric = os.path.join(current_dir, "yourfile.srt") 
    
    run_srt_pyautogui_bot(file_lyric)
