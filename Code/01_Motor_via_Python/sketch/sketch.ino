#include <Stepper.h>

const int stepsPerRevolution = 2048; // 32 Schritte � 64 Untersetzung
Stepper myStepper(stepsPerRevolution, 2, 3, 4, 5);

bool running = false;
int speed = 0;  // U/min
unsigned long lastTime = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.startsWith("SPEED")) {
      int sliderValue = input.substring(6).toInt(); // 0-100%
      if (sliderValue < 0) sliderValue = 0;
      if (sliderValue > 100) sliderValue = 100;

      // Maximalgeschwindigkeit 6 U/min
      speed = (sliderValue * 6) / 100; 
      myStepper.setSpeed(speed);
    }
    else if (input == "START") {
      running = true;
    }
    else if (input == "STOP") {
      running = false;
    }
  }

  unsigned long startLoop = micros();

  if (running && speed > 0) {
    myStepper.step(1); // 1 Schritt pro Loop
  }

  // Zykluszeit alle 100ms senden
  unsigned long cycleTime = micros() - startLoop;
  if (millis() - lastTime > 100) {
    Serial.print("CYCLE ");
    Serial.println(cycleTime);
    lastTime = millis();
  }
}
