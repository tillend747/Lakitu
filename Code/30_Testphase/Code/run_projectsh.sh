#!/bin/bash

# 1. Arduino-Sketch hochladen
echo " Lade Arduino-Sketch hoch..."
arduino-cli compile --fqbn arduino:avr:uno /home/till/Lakitu/sketch
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno /home/till/Test_PWM/sketch

# 2. Python-Script starten
echo " Starte Python-Skript..."
python3 /home/till/Test_PWM/python3 moto_gui.py
