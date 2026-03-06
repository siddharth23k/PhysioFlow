
import ipywidgets as widgets
from IPython.display import display

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

# In[3]:
import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

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

cap = cv2.VideoCapture(0)

# ==== Exercise Parameters ====
counter = 0
feedback = ""
baseline_set = False
calibration_frames = 0
calibration_sum = 0
tilt_threshold = 0.025
current_phase = None
phase_history = []

# ==== UI Parameters ====
panel_width = 400
panel_height = 100
instruction_panel_height = 160
corner_radius = 20
bg_color = (30, 30, 30)
text_color = (255, 255, 255)
accent_color = (0, 200, 255)
progress_color = (0, 255, 200)

# ==== Pose Detection ====
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

        h, w, _ = image.shape

        # ==== Top Instruction Panel ====
        top_panel_x = (w - panel_width) // 2
        top_panel_y = 20
        instruction_overlay = image.copy()
        draw_rounded_rectangle(
            instruction_overlay,
            (top_panel_x, top_panel_y),
            (top_panel_x + panel_width, top_panel_y + instruction_panel_height),
            corner_radius, bg_color, -1
        )
        cv2.addWeighted(instruction_overlay, 0.8, image, 0.2, 0, image)

        cv2.putText(image, "PELVIC TILT EXERCISE",
                    (top_panel_x + panel_width//2 - 120, top_panel_y + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, accent_color, 1, cv2.LINE_AA)

        instructions = [
            "1. Lie on your back, knees bent, feet flat",
            "2. Flatten your lower back against the floor",
            "3. Gently tilt your pelvis upward (posterior tilt)",
            "4. Hold briefly, then return to neutral",
            "5. Repeat for desired reps"
        ]

        for i, instr in enumerate(instructions):
            y_pos = top_panel_y + 60 + i * 22
            cv2.putText(image, instr, (top_panel_x + 25, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, text_color, 1, cv2.LINE_AA)

        # ==== Bottom Counter Panel ====
        bottom_panel_x = (w - panel_width) // 2
        bottom_panel_y = h - panel_height - 20
        counter_overlay = image.copy()
        draw_rounded_rectangle(
            counter_overlay,
            (bottom_panel_x, bottom_panel_y),
            (bottom_panel_x + panel_width, bottom_panel_y + panel_height),
            corner_radius, bg_color, -1
        )
        cv2.addWeighted(counter_overlay, 0.8, image, 0.2, 0, image)

        cv2.putText(image, "REPS COMPLETED",
                    (bottom_panel_x + panel_width//2 - 90, bottom_panel_y + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 1, cv2.LINE_AA)
        cv2.putText(image, str(counter),
                    (bottom_panel_x + panel_width//2 - (15 if counter < 10 else 25), bottom_panel_y + 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, text_color, 2, cv2.LINE_AA)

        if feedback:
            cv2.putText(image, feedback,
                        (bottom_panel_x + 20, bottom_panel_y + 95),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, accent_color, 1, cv2.LINE_AA)

        # ==== Pose & Reps Logic ====
        try:
            landmarks = results.pose_landmarks.landmark
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
            left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
            right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]

            mid_hip_y = (left_hip.y + right_hip.y) / 2
            mid_knee_y = (left_knee.y + right_knee.y) / 2
            pelvis_to_knee = mid_hip_y - mid_knee_y

            if not baseline_set:
                if calibration_frames < 30:
                    calibration_sum += pelvis_to_knee
                    calibration_frames += 1
                    feedback = f"Calibrating... {calibration_frames}/30"
                else:
                    baseline = calibration_sum / calibration_frames
                    baseline_set = True
                    feedback = "Ready. Begin Pelvic Tilts!"
            else:
                movement = pelvis_to_knee - baseline
                current_phase = 'Tilted' if movement > tilt_threshold else 'Neutral'
                phase_history.append(current_phase)
                if len(phase_history) > 3:
                    phase_history.pop(0)
                if len(phase_history) == 3 and phase_history == ['Neutral', 'Tilted', 'Neutral']:
                    counter += 1
                    feedback = "Rep Completed!"
                    phase_history.clear()

        except:
            pass

        # ==== Visualize Landmarks ====
        if results.pose_landmarks:
            try:
                landmarks_overlay = image.copy()
                lh = (int(left_hip.x * w), int(left_hip.y * h))
                rh = (int(right_hip.x * w), int(right_hip.y * h))
                lk = (int(left_knee.x * w), int(left_knee.y * h))
                rk = (int(right_knee.x * w), int(right_knee.y * h))
                for point in [lh, rh]:
                    cv2.circle(landmarks_overlay, point, 7, accent_color, -1)
                for point in [lk, rk]:
                    cv2.circle(landmarks_overlay, point, 7, progress_color, -1)
                cv2.line(landmarks_overlay, lh, lk, accent_color, 2)
                cv2.line(landmarks_overlay, rh, rk, accent_color, 2)
                cv2.line(landmarks_overlay, lh, rh, (200, 200, 0), 2)
                cv2.line(landmarks_overlay, lk, rk, (200, 200, 0), 2)
                cv2.addWeighted(landmarks_overlay, 0.3, image, 0.7, 0, image)
            except:
                pass

        cv2.imshow('Pelvic Tilt Tracker', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# %%
