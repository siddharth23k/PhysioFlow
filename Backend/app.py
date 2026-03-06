from flask import Flask, request, jsonify
from flask_cors import CORS
from groq_service import get_groq_feedback

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/get-groq-feedback", methods=["POST"])
def groq_feedback():
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    if not prompt:
        return jsonify({"error": "Prompt missing"}), 400
    
    try:
        groq_response = get_groq_feedback(prompt)
        return jsonify({"response": groq_response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/track-movement', methods=['POST'])
def track_movement():
    data = request.json  # Expecting keypoints or analysis input from frontend
    # Placeholder logic — replace with your OpenCV or ML logic
    result = {
        "status": "received",
        "analysis": "Movement tracking functionality will be implemented here."
    }
    return jsonify(result), 200


if __name__ == '__main__':
    app.run(port=5001, debug=True)