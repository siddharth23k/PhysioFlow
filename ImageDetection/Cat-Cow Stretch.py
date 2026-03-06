import cv2
import mediapipe as mp
import numpy as np
import argparse
import sys
import time

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Cat-Cow Stretch Tracker')
    parser.add_argument('--camera', type=int, default=0, help='Camera index to use')
    parser.add_argument('--fullscreen', action='store_true', help='Run in fullscreen mode')
    return parser.parse_args()

def draw_rounded_rectangle(img, top_left, bottom_right, radius, color, thickness=-1):
    """Draw a rectangle with rounded corners."""
    # Import here to ensure cv2 is available
    import cv2
    
    x1, y1 = top_left
    x2, y2 = bottom_right
    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y1 + radius), color, thickness)
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, thickness)
    cv2.rectangle(img, (x1 + radius, y2 - radius), (x2 - radius, y2), color, thickness)
    cv2.circle(img, (x1 + radius, y1 + radius), radius, color, thickness)
    cv2.circle(img, (x2 - radius, y1 + radius), radius, color, thickness)
    cv2.circle(img, (x1 + radius, y2 - radius), radius, color, thickness)
    cv2.circle(img, (x2 - radius, y2 - radius), radius, color, thickness)

def main():
    # Ensure all necessary packages are imported
    import cv2
    import mediapipe as mp
    import numpy as np
    
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
    window_name = 'Cat-Cow Stretch Tracker'
    if args.fullscreen:
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    else:
        cv2.namedWindow(window_name)
    
    # Exercise parameters
    counter = 0
    stage = None
    feedback = ""
    baseline_set = False
    calibration_frames = 0
    calibration_sum = 0
    cow_threshold = 0.03
    cat_threshold = 0.02
    current_phase = None
    phase_history = []
    baseline = 0
    
    # UI parameters
    panel_width = 400
    panel_height = 100
    instruction_panel_height = 160
    corner_radius = 20
    bg_color = (30, 30, 30)
    text_color = (255, 255, 255)
    accent_color = (0, 200, 255)
    progress_color = (0, 255, 200)
    
    print("\nCat-Cow Stretch Tracker")
    print("----------------------")
    print("Press 'r' to reset counter")
    print("Press 'c' to recalibrate")
    print("Press 'q' to quit")
    print("Press 'f' to toggle fullscreen")
    
    camera_active = True
    start_time = time.time()
    
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
                cv2.putText(image, "CAT-COW STRETCH", 
                           (top_panel_x + panel_width//2 - 100, top_panel_y + 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, accent_color, 1, cv2.LINE_AA)
                instructions = [
                    "1. Start on hands and knees or sit upright",
                    "2. ARCH BACK (Cow): Lift head/tailbone up",
                    "3. ROUND SPINE (Cat): Tuck chin/pelvis in",
                    "4. Move slowly through full range",
                    "5. Complete cycles for reps"
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
                cv2.putText(image, "q:quit r:reset c:calibrate f:fullscreen", 
                           (bottom_panel_x, h - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1, cv2.LINE_AA)
                
                # Counter Display
                cv2.putText(image, "REPS COMPLETED",
                           (bottom_panel_x + panel_width//2 - 90, bottom_panel_y + 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 1, cv2.LINE_AA)
                cv2.putText(image, str(counter),
                           (bottom_panel_x + panel_width//2 - (15 if counter < 10 else 25), bottom_panel_y + 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, text_color, 2, cv2.LINE_AA)
                
                # Feedback Text
                if feedback:
                    cv2.putText(image, feedback,
                               (bottom_panel_x + 20, bottom_panel_y + 95),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, accent_color, 1, cv2.LINE_AA)
            except Exception as e:
                print(f"Error drawing UI: {e}")

            # ========== EXERCISE LOGIC ========== #
            try:
                if results and results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    
                    # Key landmarks
                    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
                    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
                    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
                    
                    # Mid-spine approximation
                    mid_spine_x = (left_shoulder.x + right_shoulder.x + left_hip.x + right_hip.x) / 4
                    mid_spine_y = (left_shoulder.y + right_shoulder.y + left_hip.y + right_hip.y) / 4
                    
                    # Spinal position calculation
                    shoulder_avg_y = (left_shoulder.y + right_shoulder.y) / 2
                    hip_avg_y = (left_hip.y + right_hip.y) / 2
                    spine_position = mid_spine_y - ((shoulder_avg_y + hip_avg_y) / 2)

                    # Calibration
                    if not baseline_set:
                        if calibration_frames < 30:
                            calibration_sum += spine_position
                            calibration_frames += 1
                            feedback = f"Calibrating... {calibration_frames}/30"
                        else:
                            baseline = calibration_sum / calibration_frames
                            baseline_set = True
                            feedback = "Ready. Begin Cat-Cow!"
                    else:
                        # Phase detection
                        movement = spine_position - baseline
                        if movement < -cow_threshold:
                            current_phase = 'Cow'
                            feedback = "Cow position (arch back)"
                        elif movement > cat_threshold:
                            current_phase = 'Cat'
                            feedback = "Cat position (round spine)"
                        else:
                            current_phase = 'Neutral'
                            feedback = "Neutral position"
                        
                        # Update phase history
                        phase_history.append(current_phase)
                        if len(phase_history) > 5:
                            phase_history.pop(0)
                        
                        # Rep counting
                        if len(phase_history) >= 4:
                            if (phase_history[-4] == 'Cow' and
                                phase_history[-3] == 'Neutral' and
                                phase_history[-2] == 'Cat' and
                                phase_history[-1] == 'Neutral'):
                                counter += 1
                                feedback = "Rep Completed!"
                                phase_history.clear()

                    # ========== VISUALIZATION ========== #
                    try:
                        landmarks_overlay = image.copy()
                        
                        # Draw spine curve
                        shoulder_mid = (int((left_shoulder.x + right_shoulder.x)/2 * w),
                                      int((left_shoulder.y + right_shoulder.y)/2 * h))
                        hip_mid = (int((left_hip.x + right_hip.x)/2 * w),
                                  int((left_hip.y + right_hip.y)/2 * h))
                        mid_spine_pt = (int(mid_spine_x * w), int(mid_spine_y * h))
                        
                        curve_points = np.array([shoulder_mid, mid_spine_pt, hip_mid], dtype=np.int32)
                        cv2.polylines(landmarks_overlay, [curve_points], False, progress_color, 2)
                        
                        # Draw key points
                        for point in [shoulder_mid, mid_spine_pt, hip_mid]:
                            cv2.circle(landmarks_overlay, point, 5, accent_color, -1)
                        
                        landmarks_alpha = 0.3
                        cv2.addWeighted(landmarks_overlay, landmarks_alpha, image, 1 - landmarks_alpha, 0, image)
                        
                        # Draw phase indicator
                        if current_phase:
                            phase_pos_x = w - 150
                            phase_pos_y = 50
                            cv2.putText(image, f"Phase: {current_phase}", 
                                      (phase_pos_x, phase_pos_y),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, accent_color, 1, cv2.LINE_AA)
                    except Exception as e:
                        print(f"Error drawing landmarks: {e}")
                else:
                    # No landmarks detected
                    cv2.putText(image, "No pose detected", 
                              (w//2 - 80, h//2),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
            except Exception as e:
                print(f"Error processing landmarks: {e}")

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
                print("Counter reset")
            elif key == ord('c'):
                print("Recalibrating...")
                baseline_set = False
                calibration_frames = 0
                calibration_sum = 0
                phase_history.clear()
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
    print(f"Total Cat-Cow reps completed: {counter}")
    session_time = time.time() - start_time
    minutes, seconds = divmod(int(session_time), 60)
    print(f"Session duration: {minutes} minutes, {seconds} seconds")

if __name__ == "__main__":
    main()