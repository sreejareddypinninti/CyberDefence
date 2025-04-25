from flask import Flask, send_from_directory, jsonify, redirect, request
from flask_cors import CORS
import subprocess
import os
import sys
import atexit
import signal

app = Flask(__name__, static_folder='.', static_url_path='/')
CORS(app)

BASE_DIR = r"C:\Users\koosuru_vardhini\tasks\honeypot\Honeypot-Implementation-master"
keylogger_process = None
capture_image_process = None

def cleanup_processes():
    global keylogger_process, capture_image_process
    for proc in (keylogger_process, capture_image_process):
        if proc and proc.poll() is None:
            try:
                print(f"Terminating process {proc.pid}")
                os.kill(proc.pid, signal.SIGTERM)
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                print(f"Force killing process {proc.pid}")
                os.kill(proc.pid, signal.SIGKILL)
            except Exception as e:
                print(f"Error terminating process {proc.pid}: {e}")

atexit.register(cleanup_processes)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index1.html')

@app.route('/kmit')
def serve_kmit():
    return send_from_directory('.', 'kmit.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() if request.is_json else request.form
    username = data.get('username')
    password = data.get('psw')
    with open('data.json', 'r') as f:
        import json
        credentials = json.load(f)
    if username == credentials.get('username1') and password == credentials.get('password1'):
        return jsonify({"status": "success", "message": "Login Successful"}), 200
    return jsonify({"status": "failure", "message": "Invalid credentials", "attempts_left": 2}), 401

@app.route('/run-capture-image', methods=['POST'])
def run_capture_image():
    global capture_image_process
    try:
        script_path = os.path.join(BASE_DIR, 'CaptureImage.py')
        capture_image_process = subprocess.Popen(
            [sys.executable, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False
        )
        stdout, stderr = capture_image_process.communicate()
        return jsonify({
            "status": "success",
            "output": stdout,
            "error": stderr
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/run-keylogger', methods=['POST'])
def run_keylogger():
    global keylogger_process
    try:
        script_path = os.path.join(BASE_DIR, 'keylogger.py')
        keylogger_process = subprocess.Popen(
            [sys.executable, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False
        )
        return jsonify({
            "status": "success",
            "message": "Keylogger started"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        cleanup_processes()
    except Exception as e:
        print(f"Flask app error: {e}")
        cleanup_processes()
    finally:
        cleanup_processes()