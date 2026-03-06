# continuous_posture_analysis.py
import cv2
import base64
import requests
import time
import os
import threading
import numpy as np
from io import BytesIO
from PIL import Image
import json
import pyttsx3

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

# Your Groq API key (store in environment variable for security)
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', 'your_groq_api_key_here')

class PostureAnalyzer:
    def __init__(self, exercise_id='default', analysis_interval=5):
        self.exercise_id = exercise_id
        self.analysis_interval = analysis_interval  # seconds between analyses
        self.last_analysis_time = 0
        self.feedback_queue = []
        self.running = False
        self.cap = None
        self.feedback_thread = None
        
    def start(self, camera_idx=0):
        """Start the camera and analysis"""
        self.cap = cv2.VideoCapture(camera_idx)
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            return False
        
        self.running = True
        self.feedback_thread = threading.Thread(target=self._feedback_worker)
        self.feedback_thread.daemon = True
        self.feedback_thread.start()
        
        print(f"Starting posture analysis for {self.exercise_id}")
        return True
        
    def stop(self):
        """Stop the analysis"""
        self.running = False
        if self.cap:
            self.cap.release()
        
        # Wait for feedback thread to complete
        if self.feedback_thread:
            self.feedback_thread.join(timeout=2)
            
        print("Posture analysis stopped")
        
    def _analyze_frame(self, frame):
        """Send frame to Groq API for analysis"""
        try:
            # Convert frame to jpg image
            _, buffer = cv2.imencode('.jpg', frame)
            img_bytes = buffer.tobytes()
            
            # Convert to base64
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            # Create prompt for posture analysis
            prompt = f"""
            You are a professional fitness trainer analyzing the posture for {self.exercise_id} exercise.
            Provide brief and specific feedback (1-2 sentences) about the form and one improvement suggestion.
            Focus on the most important issue you can see.
            """
            
            data = {
                "model": "llama3-70b-8192",  # Or whatever Groq model you're using
                "messages": [
                    {"role": "system", "content": "You are a helpful fitness posture analyst."},
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                    ]}
                ],
                "temperature": 0.2,
                "max_tokens": 100
            }
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = result['choices'][0]['message']['content']
                return analysis
            else:
                print(f"Error from Groq API: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error analyzing frame: {str(e)}")
            return None
    
    def _feedback_worker(self):
        """Worker thread to speak feedback"""
        while self.running:
            if self.feedback_queue:
                feedback = self.feedback_queue.pop(0)
                print(f"Speaking: {feedback}")
                
                # Convert feedback to speech
                tts_engine.say(feedback)
                tts_engine.runAndWait()
                
                # Wait a bit to avoid overwhelming the user
                time.sleep(2)
            else:
                time.sleep(0.5)
    
    def process_frames(self):
        """Main loop to process camera frames"""
        if not self.cap:
            print("Camera not initialized")
            return
            
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error reading frame")
                break
                
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Display the frame
            cv2.imshow('Exercise Tracking', frame)
            
            # Check if it's time for analysis
            current_time = time.time()
            if current_time - self.last_analysis_time >= self.analysis_interval:
                self.last_analysis_time = current_time
                
                # Create a thread to analyze the frame
                analysis_thread = threading.Thread(
                    target=self._analyze_and_queue_feedback,
                    args=(frame.copy(),)
                )
                analysis_thread.daemon = True
                analysis_thread.start()
            
            # Break loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        # Cleanup
        cv2.destroyAllWindows()
        self.stop()
    
    def _analyze_and_queue_feedback(self, frame):
        """Analyze frame and queue feedback"""
        feedback = self._analyze_frame(frame)
        if feedback:
            # Only queue if we don't have too many waiting feedbacks
            if len(self.feedback_queue) < 2:
                self.feedback_queue.append(feedback)

# Example usage
if __name__ == "__main__":
    # Get exercise ID from command line if provided
    import sys
    exercise_id = sys.argv[1] if len(sys.argv) > 1 else "squat"
    
    analyzer = PostureAnalyzer(exercise_id=exercise_id, analysis_interval=10)
    if analyzer.start():
        try:
            analyzer.process_frames()
        except KeyboardInterrupt:
            print("Interrupted by user")
        finally:
            analyzer.stop()