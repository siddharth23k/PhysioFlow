#!/usr/bin/env python
# coding: utf-8

# Install dependencies if running in notebook


import cv2
import mediapipe as mp
import numpy as np
from IPython.display import display
import ipywidgets as widgets

# Initialize UI
camera_active = True
stop_button = widgets.Button(description='Stop Camera', button_style='danger', icon='stop')

def on_stop_button_clicked(b):
    global camera_active
    camera_active = False
    print("Camera stopped. Run the cell again to restart.")

stop_button.on_click(on_stop_button_clicked)
display(stop_button)

# Initialize Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# UI and Color Configs
UI_CONFIG = {
    "panel_width": 400,
    "panel_height": 100,
    "instruction_height": 160,
    "corner_radius": 20,
    "bg_color": (30, 30, 30),
    "text_color": (255, 255, 255),
    "accent_color": (0, 200, 255),
    "progress_color": (0, 255, 200),
    "debug": False
}

# Utility to draw rounded rectangles
def draw_rounded_rectangle(img, top_left, bottom_right, radius, color, thickness=-1):
    x1, y1 = top_left
    x2, y2 = bottom_right
    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), color, thickness)
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, thickness)
    for dx in [0, 1]:
        for dy in [0, 1]:
            corner = (x1 + radius if dx == 0 else x2 - radius, y1 + radius if dy == 0 else y2 - radius)
            cv2.circle(img, corner, radius, color, thickness)

# Shoulder Shrug Tracker Class
class ShoulderShrugTracker:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.feedback = "Initializing..."
        self.baseline_left_y = 0
        self.baseline_right_y = 0
        self.baseline_set = False
        self.calibration_frames = 0
        self.calibration_sum_left = 0
        self.calibration_sum_right = 0
        self.shrug_threshold = 0.015
        self.cap = cv2.VideoCapture(0)

    def calibrate(self, l_shoulder_y, r_shoulder_y):
        self.calibration_sum_left += l_shoulder_y
        self.calibration_sum_right += r_shoulder_y
        self.calibration_frames += 1
        self.feedback = f"Calibrating... {self.calibration_frames}/30"
        if self.calibration_frames >= 30:
            self.baseline_left_y = self.calibration_sum_left / self.calibration_frames
            self.baseline_right_y = self.calibration_sum_right / self.calibration_frames
            self.baseline_set = True
            self.feedback = "Ready. Shrug your shoulders!"

    def update_shrug_state(self, l_y, r_y):
        avg_delta = (l_y - self.baseline_left_y + r_y - self.baseline_right_y) / 2
        if UI_CONFIG["debug"]:
            print(f"L: {l_y:.4f}, R: {r_y:.4f}, Avg delta: {avg_delta:.4f}")

        if avg_delta < -self.shrug_threshold and (self.stage == 'down' or self.stage is None):
            self.stage = 'up'
            self.feedback = "Shoulders up - good!"
        elif avg_delta > -0.005 and self.stage == 'up':
            self.stage = 'down'
            self.counter += 1
            self.feedback = "Rep counted!"
        elif self.stage is None:
            self.stage = 'down'
            self.feedback = "Ready to start"

        if self.stage == 'up':
            shoulder_gauge = max(0, min(100, -avg_delta / (self.shrug_threshold * 3) * 100))
            self.feedback = f"Hold shrug: {int(shoulder_gauge)}%"
        elif self.stage == 'down' and self.counter > 0:
            self.feedback = "Return to rest position"

    def render_ui(self, image, h, w):
        top_x = (w - UI_CONFIG["panel_width"]) // 2
        top_y = 20
        bot_y = h - UI_CONFIG["panel_height"] - 20

        overlay = image.copy()
        draw_rounded_rectangle(
            overlay,
            (top_x, top_y),
            (top_x + UI_CONFIG["panel_width"], top_y + UI_CONFIG["instruction_height"]),
            UI_CONFIG["corner_radius"],
            UI_CONFIG["bg_color"]
        )
        alpha = 0.8
        cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

        instructions = [
            "1. Stand facing the camera in a relaxed position",
            "2. Lift both shoulders up toward your ears",
            "3. Hold briefly at the top position",
            "4. Lower shoulders back to resting position",
            "5. Repeat for desired number of repetitions"
        ]
        for i, text in enumerate(instructions):
            cv2.putText(image, text, (top_x + 20, top_y + 60 + 22 * i),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, UI_CONFIG["text_color"], 1)

        # Bottom counter panel
        bot_overlay = image.copy()
        draw_rounded_rectangle(
            bot_overlay,
            (top_x, bot_y),
            (top_x + UI_CONFIG["panel_width"], bot_y + UI_CONFIG["panel_height"]),
            UI_CONFIG["corner_radius"],
            UI_CONFIG["bg_color"]
        )
        cv2.addWeighted(bot_overlay, alpha, image, 1 - alpha, 0, image)
        cv2.putText(image, "SHOULDER SHRUGS", (top_x + 90, bot_y + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, UI_CONFIG["text_color"], 1)
        cv2.putText(image, str(self.counter), (top_x + 160, bot_y + 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, UI_CONFIG["text_color"], 2)
        cv2.putText(image, self.feedback, (top_x + 20, bot_y + 85),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, UI_CONFIG["accent_color"], 1)

    def run(self):
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while self.cap.isOpened() and camera_active:
                ret, frame = self.cap.read()
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
                    l_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                    r_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
                    l_y, r_y = l_shoulder.y, r_shoulder.y

                    if not self.baseline_set:
                        self.calibrate(l_y, r_y)
                    else:
                        self.update_shrug_state(l_y, r_y)

                    h, w, _ = image.shape
                    self.render_ui(image, h, w)

                except Exception as e:
                    if UI_CONFIG["debug"]:
                        print(f"Exception: {e}")

                cv2.imshow("Shoulder Shrug Tracker", image)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            self.cap.release()
            cv2.destroyAllWindows()

# Run the tracker
tracker = ShoulderShrugTracker()
tracker.run()
