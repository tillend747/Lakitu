#!/bin/bash

# 1. Arduino-Sketch hochladen
echo " Lade Arduino-Sketch hoch..."
arduino-cli compile --fqbn arduino:avr:uno /home/till/Lakitu/sketch_12
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno /home/till/12_MotorESC_via_Web/sketch_12

# 2. Python-Script starten
echo " Starte Python-Skript..."
python3 /home/till/Lakitu/12_Motor_ESC_via_Web/motor_control.py