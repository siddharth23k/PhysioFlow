#!/usr/bin/env python
# coding: utf-8

# Import required libraries
import cv2
import mediapipe as mp
import numpy as np
import time
import ipywidgets as widgets
from IPython.display import display

# Install required packages (run only if needed)
# !pip install mediapipe opencv-python

# -----------------------------
# UI: Stop Camera Button
# -----------------------------
camera_active = True

stop_button = widgets.Button(
    description='Stop Camera',
    button_style='danger',
    icon='stop'
)

def on_stop_button_clicked(b):
    global camera_active
    camera_active = False
    print("Camera stopped. Run the cell again to restart.")

stop_button.on_click(on_stop_button_clicked)
display(stop_button)

# -----------------------------
# Angle Calculation Function
# -----------------------------
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180 else angle

# -----------------------------
# Rounded Rectangle Function
# -----------------------------
def draw_rounded_rectangle(img, top_left, bottom_right, radius, color, thickness=-1):
    x1, y1 = top_left
    x2, y2 = bottom_right

    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y1 + radius), color, thickness)
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, thickness)
    cv2.rectangle(img, (x1 + radius, y2 - radius), (x2 - radius, y2), color, thickness)
    
    cv2.circle(img, (x1 + radius, y1 + radius), radius, color, thickness)
    cv2.circle(img, (x2 - radius, y1 + radius), radius, color, thickness)
    cv2.circle(img, (x1 + radius, y2 - radius), radius, color, thickness)
    cv2.circle(img, (x2 - radius, y2 - radius), radius, color, thickness)

# -----------------------------
# Initialize Variables
# -----------------------------
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

counter = 0
stage = None
squat_depth = 0
max_depth_reached = 0
feedback = ""

# UI Settings
panel_width = 250
panel_height = 100
corner_radius = 20
bg_color = (30, 30, 30)
text_color = (255, 255, 255)
accent_color = (0, 200, 255)
progress_color = (0, 255, 200)

debug_mode = False

# -----------------------------
# Start Pose Tracking
# -----------------------------
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened() and camera_active:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            def get_coords(side):
                return [
                    [landmarks[getattr(mp_pose.PoseLandmark, f"{side}_HIP").value].x,
                     landmarks[getattr(mp_pose.PoseLandmark, f"{side}_HIP").value].y],
                    [landmarks[getattr(mp_pose.PoseLandmark, f"{side}_KNEE").value].x,
                     landmarks[getattr(mp_pose.PoseLandmark, f"{side}_KNEE").value].y],
                    [landmarks[getattr(mp_pose.PoseLandmark, f"{side}_ANKLE").value].x,
                     landmarks[getattr(mp_pose.PoseLandmark, f"{side}_ANKLE").value].y],
                    [landmarks[getattr(mp_pose.PoseLandmark, f"{side}_SHOULDER").value].x,
                     landmarks[getattr(mp_pose.PoseLandmark, f"{side}_SHOULDER").value].y]
                ]

            right_hip, right_knee, right_ankle, right_shoulder = get_coords("RIGHT")
            left_hip, left_knee, left_ankle, left_shoulder = get_coords("LEFT")

            right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
            left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
            knee_angle = (right_knee_angle + left_knee_angle) / 2

            right_hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)
            left_hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
            hip_angle = (right_hip_angle + left_hip_angle) / 2

            squat_depth = min(100, max(0, (170 - knee_angle) * 100 / 80))

            if debug_mode:
                cv2.putText(image, f"Knee: {int(knee_angle)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)
                cv2.putText(image, f"Hip: {int(hip_angle)}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)

            if stage == "down":
                max_depth_reached = max(max_depth_reached, squat_depth)

            if knee_angle > 150 and hip_angle > 160:
                if stage == 'down' and max_depth_reached > 40:
                    stage = "up"
                    counter += 1
                    feedback = f"Rep counted! Depth: {int(max_depth_reached)}%"
                    max_depth_reached = 0
                elif stage != 'down':
                    stage = "up"
                    feedback = "Ready"
            elif knee_angle < 140:
                if stage == 'up' or stage is None:
                    stage = "down"
                feedback = f"Depth: {int(squat_depth)}%"

        except:
            pass

        # UI Panel
        h, w, _ = image.shape
        panel_x = (w - panel_width) // 2
        panel_y = h - panel_height - 20

        overlay = image.copy()
        draw_rounded_rectangle(overlay, (panel_x, panel_y), (panel_x + panel_width, panel_y + panel_height), corner_radius, bg_color)
        alpha = 0.8
        cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

        # Progress bar
        filled_width = int((squat_depth / 100) * (panel_width - 40))
        cv2.rectangle(image, (panel_x + 20, panel_y + panel_height - 20), (panel_x + 20 + filled_width, panel_y + panel_height - 14), progress_color, -1)

        # Text
        cv2.putText(image, "SQUATS", (panel_x + panel_width // 2 - 35, panel_y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 1)
        cv2.putText(image, str(counter), (panel_x + panel_width // 2 - 15, panel_y + 55), cv2.FONT_HERSHEY_SIMPLEX, 1.2, text_color, 2)
        if feedback:
            cv2.putText(image, feedback, (panel_x + 20, panel_y + 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, accent_color, 1)

        # Simplified landmarks
        if results.pose_landmarks:
            for lm_id in [mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER,
                          mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP,
                          mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.RIGHT_KNEE,
                          mp_pose.PoseLandmark.LEFT_ANKLE, mp_pose.PoseLandmark.RIGHT_ANKLE]:
                landmark = results.pose_landmarks.landmark[lm_id.value]
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(image, (cx, cy), 7, accent_color, -1)

        cv2.imshow('Squat Tracker', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
