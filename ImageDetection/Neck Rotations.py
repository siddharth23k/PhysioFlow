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
    parser = argparse.ArgumentParser(description='Neck Rotation Tracker')
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
    window_name = 'Neck Rotation Tracker'
    if args.fullscreen:
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    else:
        cv2.namedWindow(window_name)
    
    # Neck rotation counter variables
    counter = 0 
    stage = None
    rotation_angle = 0  # Track rotation angle
    feedback = ""
    max_right_rotation = 0  # Track maximum right rotation
    max_left_rotation = 0  # Track maximum left rotation
    left_done = False  # Track if left rotation is completed in the current rep
    right_done = False  # Track if right rotation is completed in the current rep
    
    # UI parameters
    panel_width = 400
    panel_height = 100
    instruction_panel_height = 160
    corner_radius = 20
    bg_color = (30, 30, 30)
    text_color = (255, 255, 255)
    accent_color = (0, 200, 255)
    progress_color = (0, 255, 200)
    
    print("\nNeck Rotation Tracker")
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
                cv2.putText(image, "NECK ROTATION EXERCISE", 
                           (top_panel_x + panel_width//2 - 120, top_panel_y + 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, accent_color, 1, cv2.LINE_AA)
                instructions = [
                    "1. Start in center position facing camera",
                    "2. Rotate head to left until detected",
                    "3. Return to center",
                    "4. Rotate head to right until detected",
                    "5. Return to center to complete one rep"
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
                
                # Add keyboard shortcuts info
                cv2.putText(image, "q:quit r:reset f:fullscreen", 
                           (bottom_panel_x, h - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1, cv2.LINE_AA)
                
                # Add "NECK ROTATIONS" label
                cv2.putText(image, "NECK ROTATIONS", 
                           (bottom_panel_x + panel_width//2 - 72, bottom_panel_y + 25), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 1, cv2.LINE_AA)
                
                # Counter in smaller font and placed below the label
                cv2.putText(image, str(counter), 
                           (bottom_panel_x + panel_width//2 - (15 if counter < 10 else 25), bottom_panel_y + 55), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, accent_color, 2, cv2.LINE_AA)
                
                # Current state and feedback
                if feedback:
                    cv2.putText(image, feedback, 
                               (bottom_panel_x + 20, bottom_panel_y + 85), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 1, cv2.LINE_AA)
                
                # Draw rotation gauge - horizontal bar with center indicator
                gauge_height = 6
                gauge_y = bottom_panel_y + panel_height - 20
                gauge_width = panel_width - 60  # Slightly narrower
                
                # Background of gauge
                cv2.rectangle(image, 
                             (bottom_panel_x + 30, gauge_y), 
                             (bottom_panel_x + 30 + gauge_width, gauge_y + gauge_height), 
                             (80, 80, 80), -1, cv2.LINE_AA)
                
                # Center marker
                center_x = bottom_panel_x + 30 + gauge_width // 2
                cv2.rectangle(image, 
                             (center_x - 1, gauge_y - 2), 
                             (center_x + 1, gauge_y + gauge_height + 2), 
                             (150, 150, 150), -1, cv2.LINE_AA)
                
                # Fill based on current rotation (-100 to +100)
                fill_start = center_x
                fill_width = int((rotation_angle / 100) * (gauge_width / 2))
                
                if rotation_angle < 0:  # Left rotation (negative value)
                    fill_start = center_x + fill_width
                    fill_width = abs(fill_width)
                
                cv2.rectangle(image, 
                             (fill_start, gauge_y), 
                             (fill_start + fill_width, gauge_y + gauge_height), 
                             progress_color, -1, cv2.LINE_AA)
                
                # Add gauge labels
                cv2.putText(image, "L", 
                           (bottom_panel_x + 30, gauge_y + gauge_height + 15), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
                
                cv2.putText(image, "R", 
                           (bottom_panel_x + 30 + gauge_width - 10, gauge_y + gauge_height + 15), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
                
                # Visualization of completed sides in current rep
                if left_done:
                    cv2.circle(image, (bottom_panel_x + 30, bottom_panel_y + 55), 5, progress_color, -1)
                if right_done:
                    cv2.circle(image, (bottom_panel_x + panel_width - 30, bottom_panel_y + 55), 5, progress_color, -1)
                
            except Exception as e:
                print(f"Error drawing UI: {e}")

            # ========== EXERCISE LOGIC ========== #
            try:
                if results and results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    
                    # Get coordinates for neck rotation detection
                    nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y]
                    left_ear = [landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x, landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].y]
                    right_ear = [landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].y]
                    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    
                    # Calculate the midpoint between shoulders (reference for center position)
                    mid_shoulders = [(left_shoulder[0] + right_shoulder[0])/2, (left_shoulder[1] + right_shoulder[1])/2]
                    
                    # Calculate horizontal position of nose relative to mid-shoulders
                    # Positive value means head is turned right, negative means left
                    relative_nose_pos = nose[0] - mid_shoulders[0]
                    
                    # Calculate the distance between ears (to normalize rotation measure)
                    ear_distance = np.linalg.norm(np.array(left_ear) - np.array(right_ear))
                    
                    # Normalize the rotation value to percentage (-100% to +100%)
                    rotation_angle = (relative_nose_pos / (ear_distance * 0.5)) * 100
                    
                    # Limit to -100 to 100 range
                    rotation_angle = max(-100, min(100, rotation_angle))
                    
                    # Display rotation angle for visualization
                    coord = tuple(np.multiply(mid_shoulders, [w, h]).astype(int))
                    coord = (coord[0], coord[1] - 30)  # Position above shoulders
                    
                    angle_overlay = image.copy()
                    cv2.circle(angle_overlay, coord, 30, accent_color, -1)
                    cv2.addWeighted(angle_overlay, 0.5, image, 0.5, 0, image)
                    
                    cv2.putText(image, f"{int(rotation_angle)}%", 
                              (coord[0]-25, coord[1]+5), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2, cv2.LINE_AA)
                    
                    # NECK ROTATION COUNTER LOGIC
                    # Threshold for considering a rotation complete
                    rotation_threshold = 40  # Percentage of full rotation
                    
                    # Center/neutral position
                    if abs(rotation_angle) < 20:
                        if stage == 'rotating':
                            stage = "center"
                            # If both left and right rotations were completed, count a rep
                            if left_done and right_done:
                                counter += 1
                                feedback = "Rep counted!"
                                left_done = False
                                right_done = False
                        elif stage is None:
                            stage = "center"
                            feedback = "Ready"
                    
                    # Rotating left or right
                    else:
                        if stage == 'center' or stage is None:
                            stage = "rotating"
                        
                        # Track left rotation
                        if rotation_angle <= -rotation_threshold:
                            left_done = True
                            feedback = f"Left rotation: {abs(int(rotation_angle))}%"
                        
                        # Track right rotation
                        elif rotation_angle >= rotation_threshold:
                            right_done = True
                            feedback = f"Right rotation: {int(rotation_angle)}%"
                        
                        # Update max rotations
                        max_left_rotation = min(max_left_rotation, rotation_angle)
                        max_right_rotation = max(max_right_rotation, rotation_angle)
                
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
                
                # Key points to show
                key_landmarks = [
                    mp_pose.PoseLandmark.NOSE,
                    mp_pose.PoseLandmark.LEFT_EAR,
                    mp_pose.PoseLandmark.RIGHT_EAR,
                    mp_pose.PoseLandmark.LEFT_EYE,
                    mp_pose.PoseLandmark.RIGHT_EYE,
                    mp_pose.PoseLandmark.LEFT_SHOULDER,
                    mp_pose.PoseLandmark.RIGHT_SHOULDER
                ]
                
                # Draw key landmarks on overlay
                for landmark_id in key_landmarks:
                    landmark = results.pose_landmarks.landmark[landmark_id.value]
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    # Draw larger circles for key points
                    cv2.circle(landmarks_overlay, (cx, cy), 5, accent_color, -1)
                
                # Draw connections between landmarks on overlay
                connections = [
                    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER),
                    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_EAR),
                    (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_EAR),
                    (mp_pose.PoseLandmark.LEFT_EAR, mp_pose.PoseLandmark.NOSE),
                    (mp_pose.PoseLandmark.RIGHT_EAR, mp_pose.PoseLandmark.NOSE),
                    (mp_pose.PoseLandmark.LEFT_EYE, mp_pose.PoseLandmark.NOSE),
                    (mp_pose.PoseLandmark.RIGHT_EYE, mp_pose.PoseLandmark.NOSE),
                    (mp_pose.PoseLandmark.LEFT_EYE, mp_pose.PoseLandmark.LEFT_EAR),
                    (mp_pose.PoseLandmark.RIGHT_EYE, mp_pose.PoseLandmark.RIGHT_EAR),
                ]
                
                for connection in connections:
                    start_point = results.pose_landmarks.landmark[connection[0].value]
                    end_point = results.pose_landmarks.landmark[connection[1].value]
                    
                    start_x, start_y = int(start_point.x * w), int(start_point.y * h)
                    end_x, end_y = int(end_point.x * w), int(end_point.y * h)
                    
                    cv2.line(landmarks_overlay, (start_x, start_y), (end_x, end_y), progress_color, 2)
                
                # Apply landmarks with transparency
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
                counter = 0
                left_done = False
                right_done = False
                stage = None
                max_left_rotation = 0
                max_right_rotation = 0
                feedback = "Counter reset"
                print("Counter reset")
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
    print(f"Total neck rotation repetitions completed: {counter}")
    print(f"Maximum left rotation achieved: {abs(int(max_left_rotation))}%")
    print(f"Maximum right rotation achieved: {int(max_right_rotation)}%")
    session_time = time.time() - start_time
    minutes, seconds = divmod(int(session_time), 60)
    print(f"Session duration: {minutes} minutes, {seconds} seconds")

if __name__ == "__main__":
    main()