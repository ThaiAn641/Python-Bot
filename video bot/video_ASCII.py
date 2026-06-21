import os
import sys
import time
import cv2
import numpy as np

print("====================================")
print("📌 Name: ThaiAn Hub")
print("🚀 Loading Title: Loading Script...")
print("✨ Subtitle: by Thái An")
print("====================================\n")

# Ultra-high density character palette for microscopic pixel transition
ASCII_CHARS = np.array(list("█▓▒░#$*+> "))

def generate_ascii_font_textures():
    """Pre-renders microscopic ASCII characters (3x5) for hyper-sharp density"""
    # 🔥 SHRUNK DOWN TO MICRO-SIZE: 3x5 pixels per character for maximum detail
    char_w, char_h = 3, 5
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.12  # Micro font scale to avoid text overlapping
    thickness = 1
    
    textures = []
    for char in ASCII_CHARS:
        img = np.zeros((char_h, char_w), dtype=np.uint8)
        # Draw micro text with antialiasing enabled
        cv2.putText(img, char, (0, char_h - 1), font, font_scale, 255, thickness, cv2.LINE_AA)
        textures.append(img)
        
    return np.array(textures), char_w, char_h

# Initialize the micro font masks globally
CHAR_TEXTURES, CHAR_W, CHAR_H = generate_ascii_font_textures()

def create_super_hd_ascii_frame(frame, width=420):
    """Processes video frames into a high-density microscopic ASCII text grid"""
    h_orig, w_orig, _ = frame.shape
    aspect_ratio = h_orig / w_orig
    
    ascii_w = width
    ascii_h = int(ascii_w * aspect_ratio * (CHAR_W / CHAR_H))
    
    # 1. Resize frame to the hyper-dense ASCII grid layout
    resized_frame = cv2.resize(frame, (ascii_w, ascii_h), interpolation=cv2.INTER_LINEAR)
    
    # 2. 🔥 EXTREME NEON COLOR BOOST: Amplify color saturation up to 200% for punchy visuals
    hsv = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2HSV).astype("float32")
    hsv[:, :, 1] *= 2.0  
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
    color_mapped = cv2.cvtColor(hsv.astype("uint8"), cv2.COLOR_HSV2BGR)
    
    # 3. Compute character indices from grayscale matrix
    gray_resized = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    char_indices = (gray_resized / 255 * (len(ASCII_CHARS) - 1)).astype(np.uint8)
    
    # 4. NumPy Block Vectorization mapping
    frame_masks = CHAR_TEXTURES[char_indices]  
    frame_masks = frame_masks.transpose(0, 2, 1, 3).reshape(ascii_h * CHAR_H, ascii_w * CHAR_W)
    
    # 5. Upscale canvas via rapid Nearest-Neighbor matching
    canvas_color = cv2.resize(color_mapped, (ascii_w * CHAR_W, ascii_h * CHAR_H), interpolation=cv2.INTER_NEAREST)
    
    # 6. Apply character mask overlay
    final_canvas = cv2.bitwise_and(canvas_color, canvas_color, mask=frame_masks)
    
    return final_canvas

def play_super_hd_ascii_video(video_path, width=420):
    if not os.path.exists(video_path):
        print(f"❌ Error: Video file not found at: {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps is None:
        fps = 30
    frame_delay = 1.0 / fps

    window_name = "ASCII Video"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    print("Press 'ESC' or 'q' to stop.")
    time.sleep(1)

    try:
        while cap.isOpened():
            start_time = time.time()
            
            ret, frame = cap.read()
            if not ret:
                break
                
            # Process frame through micro-matrix rendering pipeline
            super_hd_canvas = create_super_hd_ascii_frame(frame, width=width)
            
            cv2.imshow(window_name, super_hd_canvas)
            
            elapsed_time = time.time() - start_time
            wait_ms = int((frame_delay - elapsed_time) * 1000)
            
            key = cv2.waitKey(max(1, wait_ms)) & 0xFF
            if key == 27 or key == ord('q'):
                break
                
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("\n✅ Video process stopped cleanly.")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Your target video file name
    video_filename = "posrche.mp4" 
    video_file_path = os.path.join(current_dir, video_filename)
    
    # 🔥 THE HYPER-RESOLUTION CONFIGURATOR:
    # 350 = Super Sharp 
    # 420 = Insane Micro-Grid 
    # 500 = Hardware Killer 
    target_width = 500 
    
    play_super_hd_ascii_video(video_file_path, width=target_width)