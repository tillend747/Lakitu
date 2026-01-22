#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

Adafruit_BNO055 bno = Adafruit_BNO055(55);

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(10); }

  if (!bno.begin()) {
    Serial.println("BNO055 nicht gefunden!");
    while (1) { delay(1000); }
  }

  delay(1000);
  bno.setExtCrystalUse(true);
}

// CSV output:
// millis, qx, qy, qz, qw, ax, ay, az, gx, gy, gz
void loop() {
  unsigned long t = millis();

  imu::Quaternion quat = bno.getQuat();
  imu::Vector<3> linacc = bno.getVector(Adafruit_BNO055::VECTOR_LINEARACCEL);
  imu::Vector<3> gyro = bno.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE); // deg/s

  // gyro deg/s -> rad/s
  float gx = gyro.x() * (PI / 180.0f);
  float gy = gyro.y() * (PI / 180.0f);
  float gz = gyro.z() * (PI / 180.0f);

  // CSV output
  Serial.print(t); Serial.print(',');
  Serial.print(quat.x(), 6); Serial.print(',');
  Serial.print(quat.y(), 6); Serial.print(',');
  Serial.print(quat.z(), 6); Serial.print(',');
  Serial.print(quat.w(), 6); Serial.print(',');
  Serial.print(linacc.x(), 6); Serial.print(',');
  Serial.print(linacc.y(), 6); Serial.print(',');
  Serial.print(linacc.z(), 6); Serial.print(',');
  Serial.print(gx, 6); Serial.print(',');
  Serial.print(gy, 6); Serial.print(',');
  Serial.println(gz, 6);

  delay(10); // ~100 Hz
}
