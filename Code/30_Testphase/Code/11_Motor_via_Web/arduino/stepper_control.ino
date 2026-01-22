#include <Stepper.h>

const int stepsPerRevolution = 2048; // 28BYJ-48 mit 64:1 Untersetzung
Stepper myStepper(stepsPerRevolution, 2, 3, 4, 5);

bool running = false;
int speedRPM = 0;
unsigned long lastSend = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Arduino bereit");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd.startsWith("SPEED")) {
      int val = cmd.substring(6).toInt();
      val = constrain(val, 0, 100);
      speedRPM = map(val, 0, 100, 0, 6);
      myStepper.setSpeed(speedRPM);
    } 
    else if (cmd == "START") running = true;
    else if (cmd == "STOP")  running = false;
  }

  if (running && speedRPM > 0) {
    myStepper.step(1);
  }

  if (millis() - lastSend > 100) {
    Serial.print("CYCLE ");
    Serial.println(speedRPM);
    lastSend = millis();
  }
}
