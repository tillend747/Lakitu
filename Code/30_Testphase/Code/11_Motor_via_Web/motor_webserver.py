# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import serial, time

app = Flask(__name__)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speed', methods=['POST'])
def set_speed():
    speed = request.json.get('speed', 0)
    ser.write(f"SPEED {speed}\n".encode())
    return jsonify({'status': 'ok', 'speed': speed})

@app.route('/start', methods=['POST'])
def start_motor():
    ser.write(b"START\n")
    return jsonify({'status': 'running'})

@app.route('/stop', methods=['POST'])
def stop_motor():
    ser.write(b"STOP\n")
    return jsonify({'status': 'stopped'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
