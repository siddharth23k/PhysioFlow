#!/usr/bin/env python
# coding: utf-8

import cv2
import mediapipe as mp
import numpy as np
import argparse
import time
import sys

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Bicep Curl Counter')
    parser.add_argument('--camera', type=int, default=0, help='Camera index to use')
    parser.add_argument('--fullscreen', action='store_true', help='Run in fullscreen mode')
    return parser.parse_args()

def calculate_angle(a, b, c):
    """Calculate the angle between three points."""
    a = np.array(a) # First point
    b = np.array(b) # Mid point
    c = np.array(c) # End point
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
        
    return angle

def draw_rounded_rectangle(img, top_left, bottom_right, radius, color, thickness=-1):
    """Draw a rectangle with rounded corners."""
    x1, y1 = top_left
    x2, y2 = bottom_right
    
    # Draw the filled rectangle without corners
    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y1 + radius), color, thickness)  # Top
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, thickness)  # Middle
    cv2.rectangle(img, (x1 + radius, y2 - radius), (x2 - radius, y2), color, thickness)  # Bottom
    
    # Draw the four corner circles
    cv2.circle(img, (x1 + radius, y1 + radius), radius, color, thickness)  # Top-left
    cv2.circle(img, (x2 - radius, y1 + radius), radius, color, thickness)  # Top-right
    cv2.circle(img, (x1 + radius, y2 - radius), radius, color, thickness)  # Bottom-left
    cv2.circle(img, (x2 - radius, y2 - radius), radius, color, thickness)  # Bottom-right

def main():
    # Parse command line arguments
    args = parse_args()
    
    # Try to install required packages if they're not available
    try:
        import cv2
        import mediapipe as mp
        import numpy as np
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mediapipe", "opencv-python", "numpy"])
        # Re-import after installation
        import cv2
        import mediapipe as mp
        import numpy as np
    
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    
    # Initialize camera
    print("Opening camera...")
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print(f"Error: Could not open camera {args.camera}")
        return
    
    # Create window
    window_name = 'Bicep Curl Counter'
    if args.fullscreen:
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    else:
        cv2.namedWindow(window_name)
    
    # Counter variables for both arms
    left_counter = 0 
    left_stage = None
    right_counter = 0
    right_stage = None
    
    # UI parameters
    panel_width = 400
    panel_height = 100
    instruction_panel_height = 160
    corner_radius = 20
    bg_color = (30, 30, 30)
    text_color = (255, 255, 255)
    accent_color = (0, 200, 255)
    progress_color = (0, 255, 200)
    
    print("\nBicep Curl Counter")
    print("----------------------")
    print("Press 'r' to reset counter")
    print("Press 'q' to quit")
    print("Press 'f' to toggle fullscreen")
    
    camera_active = True
    start_time = time.time()
    
    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while camera_active:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Process the frame
            try:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = pose.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            except Exception as e:
                print(f"Error processing frame: {e}")
                continue

            h, w, _ = image.shape
            
            # ========== UI ELEMENTS ========== #
            try:
                # Instruction Panel (Top)
                top_panel_x = (w - panel_width) // 2
                top_panel_y = 20
                instruction_overlay = image.copy()
                draw_rounded_rectangle(
                    instruction_overlay,
                    (top_panel_x, top_panel_y),
                    (top_panel_x + panel_width, top_panel_y + instruction_panel_height),
                    corner_radius,
                    bg_color,
                    -1
                )
                alpha = 0.8
                cv2.addWeighted(instruction_overlay, alpha, image, 1 - alpha, 0, image)
                
                # Instruction Text
                cv2.putText(image, "BICEP CURL COUNTER", 
                           (top_panel_x + panel_width//2 - 120, top_panel_y + 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, accent_color, 1, cv2.LINE_AA)
                instructions = [
                    "1. Stand with arms at your sides",
                    "2. Curl both arms up to approximately 30°",
                    "3. Lower arms back down to 160°+",
                    "4. Keep elbows close to your body",
                    "5. Complete curls on both arms for reps"
                ]
                line_spacing = 22
                start_y = top_panel_y + 60
                for i, instr in enumerate(instructions):
                    y_pos = start_y + (i * line_spacing)
                    cv2.putText(image, instr,
                               (top_panel_x + 25, y_pos),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.45, text_color, 1, cv2.LINE_AA)

                # Add session info
                session_time = time.time() - start_time
                minutes, seconds = divmod(int(session_time), 60)
                timer_text = f"Session: {minutes:02d}:{seconds:02d}"
                cv2.putText(image, timer_text,
                           (w - 150, 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)

                # Counter Panel (Bottom)
                bottom_panel_x = (w - panel_width) // 2
                bottom_panel_y = h - panel_height - 20
                counter_overlay = image.copy()
                draw_rounded_rectangle(
                    counter_overlay,
                    (bottom_panel_x, bottom_panel_y),
                    (bottom_panel_x + panel_width, bottom_panel_y + panel_height),
                    corner_radius,
                    bg_color,
                    -1
                )
                cv2.addWeighted(counter_overlay, alpha, image, 1 - alpha, 0, image)
                
                # Draw divider
                divider_x = bottom_panel_x + panel_width // 2
                cv2.line(image, 
                        (divider_x, bottom_panel_y + 15), 
                        (divider_x, bottom_panel_y + panel_height - 15), 
                        (150, 150, 150), 2, cv2.LINE_AA)
                
                # Add keyboard shortcuts info
                cv2.putText(image, "q:quit r:reset f:fullscreen", 
                           (bottom_panel_x, h - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1, cv2.LINE_AA)
                
                # Left arm section
                cv2.putText(image, 'LEFT ARM', (bottom_panel_x + 20, bottom_panel_y + 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
                
                # Left counter with accent background
                cv2.putText(image, str(left_counter),
                           (bottom_panel_x + 50, bottom_panel_y + 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, accent_color, 2, cv2.LINE_AA)
                
                # Left stage
                stage_text = left_stage.upper() if left_stage else "READY"
                cv2.putText(image, stage_text, 
                           (bottom_panel_x + 100, bottom_panel_y + 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 1, cv2.LINE_AA)
                
                # Right arm section
                cv2.putText(image, 'RIGHT ARM', (divider_x + 20, bottom_panel_y + 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
                
                # Right counter with accent background
                cv2.putText(image, str(right_counter),
                           (divider_x + 50, bottom_panel_y + 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, accent_color, 2, cv2.LINE_AA)
                
                # Right stage
                stage_text = right_stage.upper() if right_stage else "READY"
                cv2.putText(image, stage_text, 
                           (divider_x + 100, bottom_panel_y + 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 1, cv2.LINE_AA)
                
            except Exception as e:
                print(f"Error drawing UI: {e}")

            # ========== EXERCISE LOGIC ========== #
            try:
                if results and results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    
                    # Get coordinates for LEFT arm
                    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    
                    # Get coordinates for RIGHT arm
                    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                    
                    # Calculate angles
                    left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                    right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                    
                    # Visualize angles with modern styling
                    for side, elbow, angle in [("L", left_elbow, left_angle), ("R", right_elbow, right_angle)]:
                        # Get coordinates and adjust
                        coord = tuple(np.multiply(elbow, [w, h]).astype(int))
                        
                        # Draw a semi-transparent background circle
                        angle_overlay = image.copy()
                        cv2.circle(angle_overlay, coord, 30, accent_color, -1)
                        cv2.addWeighted(angle_overlay, 0.5, image, 0.5, 0, image)
                        
                        # Add angle text
                        cv2.putText(image, f"{int(angle)}°", 
                                  (coord[0]-20, coord[1]+5), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2, cv2.LINE_AA)
                    
                    # Curl counter logic for left arm
                    if left_angle > 160:
                        left_stage = "down"
                    if left_angle < 30 and left_stage == 'down':
                        left_stage = "up"
                        left_counter += 1
                        print(f"Left arm rep: {left_counter}")
                    
                    # Curl counter logic for right arm
                    if right_angle > 160:
                        right_stage = "down"
                    if right_angle < 30 and right_stage == 'down':
                        right_stage = "up"
                        right_counter += 1
                        print(f"Right arm rep: {right_counter}")
                
                else:
                    # No landmarks detected
                    cv2.putText(image, "No pose detected", 
                              (w//2 - 80, h//2),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                
            except Exception as e:
                print(f"Error processing landmarks: {e}")

            # ========== RENDER POSE ========== #
            if results and results.pose_landmarks:
                # Create a copy for landmarks overlay
                landmarks_overlay = image.copy()
                
                # Draw pose landmarks
                mp_drawing.draw_landmarks(
                    landmarks_overlay, 
                    results.pose_landmarks, 
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                )
                
                # Blend with original image
                landmarks_alpha = 0.7
                cv2.addWeighted(landmarks_overlay, landmarks_alpha, image, 1 - landmarks_alpha, 0, image)

            # Display the frame
            try:
                cv2.imshow(window_name, image)
            except Exception as e:
                print(f"Error displaying frame: {e}")
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            # Handle key presses
            if key == ord('q'):
                print("Quitting...")
                camera_active = False
            elif key == ord('r'):
                left_counter = 0
                right_counter = 0
                left_stage = None
                right_stage = None
                print("Counters reset")
            elif key == ord('f'):
                # Toggle fullscreen
                if cv2.getWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN) == cv2.WINDOW_FULLSCREEN:
                    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
                    print("Exiting fullscreen mode")
                else:
                    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                    print("Entering fullscreen mode")

    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    print("\nSession summary:")
    print(f"Total Left Arm reps completed: {left_counter}")
    print(f"Total Right Arm reps completed: {right_counter}")
    session_time = time.time() - start_time
    minutes, seconds = divmod(int(session_time), 60)
    print(f"Session duration: {minutes} minutes, {seconds} seconds")

if __name__ == "__main__":
    main()