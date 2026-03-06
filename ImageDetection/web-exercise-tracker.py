# ============== Backend Implementation (app.py) ==============
from flask import Flask, render_template, Response, request, jsonify
import cv2
import numpy as np
import mediapipe as mp
import importlib.util
import os
import sys
import json
import base64
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Dictionary to store loaded exercise models
exercise_models = {}

# Path to the directory containing exercise model modules
MODELS_DIR = 'exercise_models'

def load_exercise_module(exercise_name):
    """Dynamically load an exercise module from the models directory"""
    try:
        # Construct path to the module file
        module_path = os.path.join(MODELS_DIR, f"{exercise_name}.py")
        
        if not os.path.exists(module_path):
            logger.error(f"Exercise module {exercise_name}.py not found")
            return None
            
        # Create a module specification
        module_name = f"exercise_models.{exercise_name}"
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        
        # Create the module
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        
        # Execute the module
        spec.loader.exec_module(module)
        
        logger.info(f"Successfully loaded module: {exercise_name}")
        return module
    except Exception as e:
        logger.error(f"Error loading exercise module {exercise_name}: {str(e)}")
        return None

# Routes for web application
@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/exercise/<exercise_name>')
def exercise_page(exercise_name):
    """Serve the specific exercise page"""
    return render_template('exercise.html', exercise_name=exercise_name)

@app.route('/api/exercises')
def list_exercises():
    """Return a list of available exercises"""
    exercises = []
    for filename in os.listdir(MODELS_DIR):
        if filename.endswith('.py') and not filename.startswith('__'):
            exercise_name = filename[:-3]  # Remove .py extension
            exercises.append({
                'id': exercise_name,
                'name': exercise_name.replace('_', ' ').title()
            })
    return jsonify(exercises)

@app.route('/api/process_frame', methods=['POST'])
def process_frame():
    """Process a single frame using the specified exercise model"""
    try:
        # Get the exercise name and base64 encoded frame from the request
        data = request.json
        exercise_name = data.get('exercise')
        base64_image = data.get('image')
        
        # Decode the base64 image
        encoded_data = base64_image.split(',')[1] if ',' in base64_image else base64_image
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Load the exercise model if not already loaded
        if exercise_name not in exercise_models:
            module = load_exercise_module(exercise_name)
            if module is None:
                return jsonify({'error': f'Exercise module {exercise_name} not found'}), 404
            
            # Create an instance of the exercise tracker class
            if hasattr(module, 'ExerciseTracker'):
                exercise_models[exercise_name] = module.ExerciseTracker()
            else:
                return jsonify({'error': f'ExerciseTracker class not found in {exercise_name} module'}), 500
        
        # Process the frame using the exercise tracker
        tracker = exercise_models[exercise_name]
        result = tracker.process_frame(img)
        
        # Encode the processed image
        _, buffer = cv2.imencode('.jpg', result['image'])
        processed_image = base64.b64encode(buffer).decode('utf-8')
        
        # Return the results
        return jsonify({
            'image': f'data:image/jpeg;base64,{processed_image}',
            'counter': result['counter'],
            'feedback': result['feedback'],
            'stage': result['stage']
        })
        
    except Exception as e:
        logger.error(f"Error processing frame: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Make sure the models directory exists
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
