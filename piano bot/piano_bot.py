import os
import time
import cv2
import numpy as np
import mido
from moviepy import VideoFileClip, AudioFileClip

print("====================================")
print("📌 Name: ThaiAn Hub")
print("✨ Subtitle: by Zoink (ThaiAn)")
print("====================================\n")

# Extended note mapping supporting sharp keys (represented as 's')
NOTES_ORDER = ['C4', 'C4s', 'D4', 'D4s', 'E4', 'F4', 'F4s', 'G4', 'G4s', 'A4', 'B4', 'C5', 'C5s', 'D5', 'D5s', 'E5', 'F5', 'F5s', 'G5']

MIDI_TO_NAME = {
    60: 'C4', 61: 'C4s', 62: 'D4', 63: 'D4s', 64: 'E4', 65: 'F4', 66: 'F4s', 
    67: 'G4', 68: 'G4s', 69: 'A4', 71: 'B4', 72: 'C5', 73: 'C5s', 74: 'D5', 
    75: 'D5s', 76: 'E5', 77: 'F5', 78: 'F5s', 79: 'G5'
}

def generate_piano_pro(midi_filename="input.mid", output_video="output.mp4"):
    if not os.path.exists(midi_filename):
        print(f"Could not find MIDI file '{midi_filename}'!")
        return

    temp_video = "temp_silent_midi.mp4"

    print(" Step 1: Parsing musical structure from MIDI file...")
    mid = mido.MidiFile(midi_filename)
    total_time = mid.length
    fps = 30
    total_frames = int(total_time * fps)
    
    width, height = 1280, 720
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))

    timeline = [set() for _ in range(total_frames)]
    audio_notes_events = []

    current_time = 0.0
    for msg in mid:
        current_time += msg.time
        frame_idx = int(current_time * fps)
        
        if frame_idx >= total_frames:
            break
            
        if msg.type == 'note_on' and msg.velocity > 0:
            if msg.note in MIDI_TO_NAME:
                note_name = MIDI_TO_NAME[msg.note]
                # Hold the key lighting effect for 6 frames (~0.2 seconds) for smooth visual effect
                for f in range(frame_idx, min(frame_idx + 6, total_frames)):
                    timeline[f].add(note_name)
                
                # Log timestamps for the acoustic piano sound synthesis
                audio_notes_events.append({
                    'note': note_name,
                    'start_time': current_time
                })

    print(" Step 2: Rendering Neon matrix piano keys video...")
    # Dynamically scale key width depending on the total notes inside the array
    key_width = max(40, width // (len(NOTES_ORDER) + 2))
    key_height = 400
    start_x = (width - (len(NOTES_ORDER) * key_width)) // 2
    start_y = 200

    for f_idx in range(total_frames):
        active_notes = timeline[f_idx]
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:] = (15, 15, 15) # Cyberpunk dark background

        cv2.putText(frame, "Piano Bot", (40, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 120), 3, cv2.LINE_AA)

        for idx, note in enumerate(NOTES_ORDER):
            x1 = start_x + (idx * key_width)
            y1 = start_y
            x2 = x1 + key_width - 2
            y2 = y1 + key_height

            # Separate natural white keys and accidental sharp keys (labeled with 's')
            is_sharp = 's' in note

            if note in active_notes:
                # Key pressed: Glowing brilliant Neon Green color
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 120), -1)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
            else:
                if is_sharp:
                    # Sharp keys default color: Dark charcoal gray
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (50, 50, 50), -1)
                else:
                    # White keys default color: Clean ivory white
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (230, 230, 230), -1)

            # Display compact note names at the bottom of the piano layout
            display_text = note.replace('4','').replace('5','').replace('s','#')
            text_color = (255, 255, 255) if is_sharp else (100, 100, 100)
            if note in active_notes: text_color = (0, 0, 0)
            cv2.putText(frame, display_text, (x1 + 5, y2 - 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)

        video_writer.write(frame)
    video_writer.release()

    print("\n Step 3: Synthesizing acoustic piano sound sequences...")
    try:
        clips_to_mix = []
        for event in audio_notes_events:
            sound_path = f"piano_sounds/{event['note']}.wav"
            if os.path.exists(sound_path):
                # Import audio sample and calibrate its exact play timestamp
                audio_sample = AudioFileClip(sound_path).with_start(event['start_time'])
                clips_to_mix.append(audio_sample)
        
        if not clips_to_mix:
            print("The directory 'piano_sounds' contains no matching audio files!")
            return

        # Mixing all parallel key strokes together using MoviePy core
        from moviepy.audio.AudioClip import CompositeAudioClip
        final_audio = CompositeAudioClip(clips_to_mix)

        print(" Step 4: Merging synchronized sound waves into video file...")
        with VideoFileClip(temp_video) as video_clip:
            final_video = video_clip.with_audio(final_audio)
            final_video.write_videofile(output_video, codec="libx264", audio_codec="aac", logger=None)
            final_video.close()

        # Delete unneeded silent temporary file
        if os.path.exists(temp_video): 
            os.remove(temp_video)
            
        print(f"\nRender completed: '{output_video}' ")

    except Exception as e:
        print(f" Audio mixing engine exception error: {e}")

if __name__ == "__main__":
    generate_piano_pro("input.mid", "output.mp4")