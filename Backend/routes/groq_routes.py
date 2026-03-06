from flask import Blueprint, request, jsonify
from pose_analyzer import generate_prompt_from_pose
from groq_service import get_groq_feedback

groq_bp = Blueprint('groq', __name__)

@groq_bp.route('/get-feedback', methods=['POST'])
def get_feedback():
    try:
        pose_data = request.json  # Pose data sent from frontend/OpenCV
        prompt = generate_prompt_from_pose(pose_data)
        feedback = get_groq_feedback(prompt)
        return jsonify({"feedback": feedback})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@groq_bp.route('/groq/ask', methods=['POST'])
def ask_groq():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    response = get_groq_feedback(prompt)
    return jsonify({'response': response})