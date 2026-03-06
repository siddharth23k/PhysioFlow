    #!/usr/bin/env python
# coding: utf-8

# Install required libraries (run once)
# !pip install mediapipe opencv-python

import cv2
import mediapipe as mp
import numpy as np
import ipywidgets as widgets
from IPython.display import display

# ========== Camera Toggle UI ==========
camera_active = True
stop_button = widgets.Button(description='Stop Camera', button_style='danger', icon='stop')

def on_stop_button_clicked(b):
    global camera_active
    camera_active = False
    print("Camera stopped. Run the cell again to restart.")

stop_button.on_click(on_stop_button_clicked)
display(stop_button)

# ========== Helper Functions ==========

def draw_rounded_rectangle(img, top_left, bottom_right, radius, color, thickness=-1):
    """Draw a rounded rectangle on an image."""
    x1, y1 = top_left
    x2, y2 = bottom_right
    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y1 + radius), color, thickness)
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, thickness)
    cv2.rectangle(img, (x1 + radius, y2 - radius), (x2 - radius, y2), color, thickness)
    cv2.circle(img, (x1 + radius, y1 + radius), radius, color, thickness)
    cv2.circle(img, (x2 - radius, y1 + radius), radius, color, thickness)
    cv2.circle(img, (x1 + radius, y2 - radius), radius, color, thickness)
    cv2.circle(img, (x2 - radius, y2 - radius), radius, color, thickness)

# ========== Tracker Initialization ==========

cap = cv2.VideoCapture(0)

counter, calibration_sum, calibration_frames = 0, 0, 0
baseline_distance, tuck_threshold = 0, 0.04
baseline_set, stage, feedback = False, None, ""

# UI configuration
panel_width, panel_height, instruction_panel_height, corner_radius = 400, 100, 160, 20
bg_color, text_color, accent_color, progress_color = (30, 30, 30), (255, 255, 255), (0, 200, 255), (0, 255, 200)

# ========== Pose Model ==========
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened() and camera_active:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Process frame
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = pose.process(image_rgb)
        image_rgb.flags.writeable = True
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        h, w, _ = image.shape

        # Pose landmarks logic
        try:
            lm = results.pose_landmarks.landmark
            nose = lm[mp_pose.PoseLandmark.NOSE.value]
            mouth_l = lm[mp_pose.PoseLandmark.MOUTH_LEFT.value]
            mouth_r = lm[mp_pose.PoseLandmark.MOUTH_RIGHT.value]
            left_sh = lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_sh = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

            chin_x, chin_y = (mouth_l.x + mouth_r.x) / 2, (mouth_l.y + mouth_r.y) / 2
            neck_x, neck_y = (left_sh.x + right_sh.x) / 2, (left_sh.y + right_sh.y) / 2
            nose_neck_dist = abs(nose.y - neck_y)

            if not baseline_set:
                if calibration_frames < 30:
                    calibration_sum += nose_neck_dist
                    calibration_frames += 1
                    feedback = f"Calibrating... {calibration_frames}/30"
                else:
                    baseline_distance = calibration_sum / calibration_frames
                    baseline_set = True
                    feedback = "Ready. Tuck your chin!"
            else:
                delta = baseline_distance - nose_neck_dist
                if delta > tuck_threshold and stage in [None, 'neutral']:
                    stage = 'tucked'
                    feedback = "Chin tucked - good!"
                elif delta < tuck_threshold / 2 and stage == 'tucked':
                    stage = 'neutral'
                    counter += 1
                    feedback = "Rep counted!"
                elif stage is None:
                    stage = 'neutral'
                    feedback = "Ready to start"
                if stage == 'tucked':
                    feedback = f"Hold tuck: {int((delta / (tuck_threshold * 2)) * 100)}%"

        except Exception:
            pass

        # ========== UI Drawing ==========
        def draw_panels():
            # Top instruction panel
            instruction_overlay = image.copy()
            draw_rounded_rectangle(instruction_overlay,
                (top_panel_x, top_panel_y),
                (top_panel_x + panel_width, top_panel_y + instruction_panel_height),
                corner_radius, bg_color)
            cv2.addWeighted(instruction_overlay, 0.8, image, 0.2, 0, image)
            cv2.putText(image, "CHIN TUCK EXERCISE", (top_panel_x + 40, top_panel_y + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, accent_color, 1)
            for i, instr in enumerate([
                "1. Sit/stand facing the camera, head neutral",
                "2. Gently tuck your chin toward your chest",
                "3. Hold briefly at the end position",
                "4. Return to neutral (look straight)",
                "5. Repeat for desired reps"
            ]):
                cv2.putText(image, instr, (top_panel_x + 25, top_panel_y + 60 + i * 22),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, text_color, 1)

            # Bottom counter panel
            counter_overlay = image.copy()
            draw_rounded_rectangle(counter_overlay,
                (bottom_panel_x, bottom_panel_y),
                (bottom_panel_x + panel_width, bottom_panel_y + panel_height),
                corner_radius, bg_color)
            cv2.addWeighted(counter_overlay, 0.8, image, 0.2, 0, image)

            # Counter + Feedback
            cv2.putText(image, "CHIN TUCKS", (bottom_panel_x + 100, bottom_panel_y + 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 1)
            cv2.putText(image, str(counter), (bottom_panel_x + 170, bottom_panel_y + 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, text_color, 2)
            cv2.putText(image, feedback, (bottom_panel_x + 20, bottom_panel_y + 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, accent_color, 1)

            # Progress bar
            gauge_x, gauge_y, gauge_height = bottom_panel_x + panel_width - 50, bottom_panel_y + 20, panel_height - 40
            cv2.rectangle(image, (gauge_x, gauge_y), (gauge_x + 6, gauge_y + gauge_height), (80, 80, 80), -1)
            if baseline_set:
                try:
                    fill = int(gauge_height * max(0, min(1, (baseline_distance - nose_neck_dist) / (tuck_threshold * 2))))
                    cv2.rectangle(image, (gauge_x, gauge_y + gauge_height - fill), (gauge_x + 6, gauge_y + gauge_height),
                                  progress_color, -1)
                except:
                    pass
            cv2.putText(image, "TUCK", (gauge_x - 10, gauge_y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1)
            cv2.putText(image, "NEUTRAL", (gauge_x - 30, gauge_y + gauge_height + 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1)

        top_panel_x, top_panel_y = (w - panel_width) // 2, 20
        bottom_panel_x, bottom_panel_y = (w - panel_width) // 2, h - panel_height - 20

        draw_panels()

        # Optional: Draw landmarks
        if results.pose_landmarks:
            overlay = image.copy()
            for idx in [mp_pose.PoseLandmark.NOSE, mp_pose.PoseLandmark.MOUTH_LEFT,
                        mp_pose.PoseLandmark.MOUTH_RIGHT, mp_pose.PoseLandmark.LEFT_SHOULDER,
                        mp_pose.PoseLandmark.RIGHT_SHOULDER]:
                lmk = results.pose_landmarks.landmark[idx.value]
                cv2.circle(overlay, (int(lmk.x * w), int(lmk.y * h)), 5, accent_color, -1)
            cv2.addWeighted(overlay, 0.2, image, 0.8, 0, image)

        # Display frame
        cv2.imshow('Chin Tuck Tracker', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Cleanup
cap.release()
cv2.destroyAllWindows()
