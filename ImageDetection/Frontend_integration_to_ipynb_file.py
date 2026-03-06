from flask import Flask, render_template, request, jsonify
from subprocess import Popen
import os
import sys

app = Flask(__name__, static_folder='./frontend/build', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/launch_notebook', methods=['POST'])
def launch_notebook():
    try:
        # Path to your notebook file
        notebook_path = os.path.join(os.getcwd(), 'your_tracking_notebook.ipynb')
        
        # Launch Jupyter notebook
        process = Popen([sys.executable, '-m', 'jupyter', 'notebook', notebook_path])
        
        return jsonify({'status': 'success', 'message': 'Notebook launched successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
