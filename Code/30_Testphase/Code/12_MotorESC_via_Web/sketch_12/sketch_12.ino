#include <Servo.h>

Servo esc;
int escPin = 9;
int throttle = 1000;
bool motorOn = false;

void setup() {
  Serial.begin(9600);
  esc.attach(escPin);
  esc.writeMicroseconds(1000);
  delay(2000); // ESC initialisieren
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "START") {
      motorOn = true;
    } else if (cmd == "STOP") {
      motorOn = false;
      esc.writeMicroseconds(1000);
    } else if (cmd.startsWith("SPD")) {
      int value = cmd.substring(3).toInt();
      throttle = constrain(value, 1000, 2000);
    }
  }

  if (motorOn) {
    esc.writeMicroseconds(throttle);
  } else {
    esc.writeMicroseconds(1000);
  }
}
