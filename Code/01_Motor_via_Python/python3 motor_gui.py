import serial
import tkinter as tk

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def send_speed(value):
    ser.write(f"SPEED {value}\n".encode())

def start_motor():
    ser.write(b"START\n")

def stop_motor():
    ser.write(b"STOP\n")

def read_cycle():
    while ser.in_waiting:
        line = ser.readline().decode().strip()
        if line.startswith("CYCLE"):
            cycle_var.set(f"Zykluszeit: {line.split()[1]} us")
    root.after(100, read_cycle)

root = tk.Tk()
root.title("28BYJ-48 Motor GUI")

tk.Label(root, text="Geschwindigkeit (%)").pack()
speed_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=send_speed)
speed_slider.pack()

start_btn = tk.Button(root, text="START", command=start_motor)
start_btn.pack()

stop_btn = tk.Button(root, text="STOP", command=stop_motor)
stop_btn.pack()

cycle_var = tk.StringVar()
cycle_var.set("Zykluszeit: --- us")
cycle_label = tk.Label(root, textvariable=cycle_var)
cycle_label.pack()

root.after(100, read_cycle)
root.mainloop()
