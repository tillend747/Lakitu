from flask import Flask, render_template_string, request
import serial

# Passe ggf. den Port an
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Brushless Motorsteuerung</title>
<style>
body { font-family: sans-serif; text-align:center; margin-top:50px; }
input[type=range] { width: 300px; }
button { font-size: 18px; margin: 10px; padding: 10px 20px; }
</style>
</head>
<body>
<h1>Brushless-Motorsteuerung</h1>
<form method="POST">
  <input type="range" name="speed" min="1000" max="2000" step="10" value="{{speed}}"><br>
  <p>Speed: {{speed}} µs</p>
  <button name="action" value="START">Start</button>
  <button name="action" value="STOP">Stop</button>
  <button name="action" value="SET">Set Speed</button>
</form>
</body>
</html>
"""

speed = 1200

@app.route('/', methods=['GET', 'POST'])
def control():
    global speed
    if request.method == 'POST':
        action = request.form['action']
        if action == 'START':
            arduino.write(b'START\n')
        elif action == 'STOP':
            arduino.write(b'STOP\n')
        elif action == 'SET':
            speed = int(request.form['speed'])
            arduino.write(f'SPD{speed}\n'.encode())
    return render_template_string(HTML, speed=speed)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
