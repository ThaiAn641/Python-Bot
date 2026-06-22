import os
import time
import cv2
import numpy as np
import random
from cvzone.PoseModule import PoseDetector
from cvzone.HandTrackingModule import HandDetector

print("====================================")
print("📌 Name: ThaiAn Hub")
print("✨ Subtitle: by Thai An")
print("====================================\n")


BODY_CONNECTIONS = [
    (11, 12), (12, 14), (14, 16), (11, 13), (13, 15),
    (11, 23), (12, 24), (23, 24),
    (23, 25), (25, 27), (27, 29), (29, 31), (27, 31),
    (24, 26), (26, 28), (28, 30), (30, 32), (28, 32)
]


HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (0, 9), (9, 10), (10, 11), (11, 12),
    (0, 13), (13, 14), (14, 15), (15, 16),
    (0, 17), (17, 18), (18, 19), (19, 20),
    (5, 9), (9, 13), (13, 17)
]

def load_user_custom_image(filename="middle_finger.png", size=(140, 140)):
    """Loads the user's custom image from folder, or creates a backup if missing."""
    if os.path.exists(filename):
        img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

        img = cv2.resize(img, size)
        return img
    else:
        
        img = np.zeros((size[1], size[0], 3), dtype=np.uint8)
        cv2.rectangle(img, (2, 2), (size[0]-2, size[1]-2), (0, 0, 255), 2)
        cv2.putText(img, "MISSING FILE", (15, 50), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), 1)
        cv2.putText(img, "middle_fingerpng", (20, 80), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 255), 1)
        return img

def overlay_transparent_image(background, overlay, x, y):
    """Safely overlays the custom image onto the camera frame, supporting transparency if available."""
    bg_h, bg_w, _ = background.shape
    ol_h, ol_w = overlay.shape[0], overlay.shape[1]

    # Calculate overlay bounding boundaries safely
    xmin, xmax = max(0, x - ol_w // 2), min(bg_w, x + ol_w // 2)
    ymin, ymax = max(0, y - ol_h - 15), min(bg_h, y - 15)

    crop_w = xmax - xmin
    crop_h = ymax - ymin

    if crop_w <= 0 or crop_h <= 0:
        return background

    # Calculate overlay source image crop offsets
    ol_xmin = 0 if (x - ol_w // 2) >= 0 else (ol_w // 2 - x)
    ol_ymin = 0 if (y - ol_h - 15) >= 0 else (ol_h + 15 - y)
    ol_xmax = ol_xmin + crop_w
    ol_ymax = ol_ymin + crop_h

    overlay_crop = overlay[ol_ymin:ol_ymax, ol_xmin:ol_xmax]

    # Blend overlay supporting both PNG (4 channels) and JPG (3 channels)
    if overlay_crop.shape[2] == 4:  # PNG alpha transparent layer
        alpha = overlay_crop[:, :, 3] / 255.0
        for c in range(3):
            background[ymin:ymax, xmin:xmax, c] = (
                alpha * overlay_crop[:, :, c] + (1.0 - alpha) * background[ymin:ymax, xmin:xmax, c]
            )
    else:  # Standard RGB image
        background[ymin:ymax, xmin:xmax] = overlay_crop[:, :, 0:3]

    # Draw a technical indicator line from finger tip to image base
    cv2.line(background, (x, y), (x, ymax), (0, 0, 255), 2, cv2.LINE_AA)
    return background

def draw_super_hyper_jointed_skeleton(img, lm_list, connections, neon_color=(0, 255, 180), is_body=False):
    """
    Hyper-Jointed Android Skeleton Engine: Multiplies bones by splitting every connection 
    into 3 sub-segments to insert 2 mechanical sub-joints per line.
    """
    glow = img.copy()
    
    # 1. LAYER 1: Neon Aura Bleeding Glow Effect
    for conn in connections:
        if conn[0] < len(lm_list) and conn[1] < len(lm_list):
            p1 = (lm_list[conn[0]][0], lm_list[conn[0]][1])
            p2 = (lm_list[conn[1]][0], lm_list[conn[1]][1])
            cv2.line(glow, p1, p2, neon_color, 8, cv2.LINE_AA)
    cv2.GaussianBlur(glow, (9, 9), 0, dst=img)
    
    # 2. LAYER 2: Core Matrix lines
    for conn in connections:
        if conn[0] < len(lm_list) and conn[1] < len(lm_list):
            p1 = (lm_list[conn[0]][0], lm_list[conn[0]][1])
            p2 = (lm_list[conn[1]][0], lm_list[conn[1]][1])
            cv2.line(img, p1, p2, (245, 255, 245), 2, cv2.LINE_AA)

    # 3. LAYER 3: INJECT DOUBLE MICRO-JOINTS PER BONE (X3 Khớp Robot Siêu Dày)
    for conn in connections:
        if conn[0] < len(lm_list) and conn[1] < len(lm_list):
            p1_x, p1_y = lm_list[conn[0]][0], lm_list[conn[0]][1]
            p2_x, p2_y = lm_list[conn[1]][0], lm_list[conn[1]][1]
            
            # Math Interpolation: Point A at 1/3 and Point B at 2/3 distance
            sub1_x = int(p1_x + (p2_x - p1_x) * 0.33)
            sub1_y = int(p1_y + (p2_y - p1_y) * 0.33)
            
            sub2_x = int(p1_x + (p2_x - p1_x) * 0.66)
            sub2_y = int(p1_y + (p2_y - p1_y) * 0.66)
            
            # Render extra micro-joints nodes (Mắt xích robot màu tím hồng neon)
            cv2.circle(img, (sub1_x, sub1_y), 4, (255, 0, 255), -1, cv2.LINE_AA)
            cv2.circle(img, (sub1_x, sub1_y), 5, (255, 120, 255), 1, cv2.LINE_AA)
            
            cv2.circle(img, (sub2_x, sub2_y), 4, (255, 0, 255), -1, cv2.LINE_AA)
            cv2.circle(img, (sub2_x, sub2_y), 5, (255, 120, 255), 1, cv2.LINE_AA)

    # 4. LAYER 4: Render primary joints nodes (No head dots)
    if is_body:
        for i in range(11, len(lm_list)):
            cx, cy = lm_list[i][0], lm_list[i][1]
            cv2.circle(img, (cx, cy), 5, (0, 255, 255), -1, cv2.LINE_AA)
            cv2.circle(img, (cx, cy), 7, (0, 100, 255), 1, cv2.LINE_AA)
    else:
        for lm in lm_list:
            cx, cy = lm[0], lm[1]
            cv2.circle(img, (cx, cy), 5, (0, 255, 255), -1, cv2.LINE_AA)
            cv2.circle(img, (cx, cy), 7, (0, 100, 255), 1, cv2.LINE_AA)

def run_v4_ultra_engine():
    cap = cv2.VideoCapture(0)
    
    # Force high definition mapping layout
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    pose_detector = PoseDetector(detectionCon=0.5, trackCon=0.5)
    hand_detector = HandDetector(detectionCon=0.55, maxHands=2) # Detects BOTH hands
    
    # Load user's customized middle finger asset photo
    middle_finger_custom = load_user_custom_image("ngongiua.png", size=(140, 140))

    window_name = "ThaiAn Hub - V4 Ultra HD Skeleton Engine"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    print("Press 'q' to shut down.\n")

    # Image enhancement sharpening kernel mask (Bộ lọc chống mờ, tăng nét camera)
    sharpen_kernel = np.array([[-1, -1, -1], 
                               [-1,  9, -1], 
                               [-1, -1, -1]])

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            
            frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=10)
            frame = cv2.filter2D(frame, -1, sharpen_kernel)
            
            # 1. PROCESS BODY SKELETON (No dots on face)
            frame = pose_detector.findPose(frame, draw=False)
            body_lms, _ = pose_detector.findPosition(frame, draw=False)
            if body_lms:
                draw_super_hyper_jointed_skeleton(frame, body_lms, BODY_CONNECTIONS, neon_color=(0, 255, 120), is_body=True)

            # 2. PROCESS PRECISION MULTI-HAND SKELETON
            hands, frame = hand_detector.findHands(frame, draw=False, flipType=False)
            
            hud_status = "MATRIX SCANNING..."
            hud_color = (0, 255, 255)

            if hands:
                hud_status = f"HYPER_TRACKING - ENGAGED ({len(hands)} HANDS)"
                
                for hand in hands:
                    hand_lms = hand["lmList"]
                    
                    # Draw hand skeleton with triple micro-joints enabled
                    draw_super_hyper_jointed_skeleton(frame, hand_lms, HAND_CONNECTIONS, neon_color=(0, 255, 240), is_body=False)
                    
                    # Check gesture state per hand
                    fingers_state = hand_detector.fingersUp(hand)
                    if fingers_state == [0, 0, 1, 0, 0]: # Middle finger only
                        hud_status = "CRITICAL WARNING: DETECTED_TARGET"
                        hud_color = (0, 0, 255)
                        
                        # Pin middle finger tip node coordinate (ID 12)
                        mx, my = hand_lms[12][0], hand_lms[12][1]
                        
                        # 🔥 OVERLAY YOUR PHOTO: Load directly above the finger tip location safely
                        frame = overlay_transparent_image(frame, middle_finger_custom, mx, my)

            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (frame_w, 55), (15, 15, 25), -1)
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
            
            cv2.line(frame, (10, 10), (30, 10), (0, 255, 180), 2)
            cv2.line(frame, (10, 10), (10, 30), (0, 255, 180), 2)
            
            cv2.putText(frame, f">> SYSTEM_STATUS: {hud_status}", (25, 35), 
                        cv2.FONT_HERSHEY_PLAIN, 1.2, hud_color, 1, cv2.LINE_AA)
            cv2.putText(frame, f"RESOLUTION: {frame_w}x{frame_h} [SHARPENED]", (frame_w - 380, 35), 
                        cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 255, 255), 1, cv2.LINE_AA)

            cv2.imshow(window_name, frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("\nEngine shut down safely.")

if __name__ == "__main__":
    run_v4_ultra_engine()
