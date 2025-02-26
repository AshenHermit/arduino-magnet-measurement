#include <SoftwareSerial.h>

// Hall sensor pins
const int digitalPin = 12; // linear Hall magnetic sensor digital interface
const int analogPin = A0;  // linear Hall magnetic sensor analog interface

// Set up a new SoftwareSerial object
SoftwareSerial mySerial(rxPin, -1);

void setup()
{
  pinMode(digitalPin, INPUT);
  pinMode(analogPin, INPUT);
  Serial.begin(9600);
}

void sendData(int sensorDigital, int sensorAnalog)
{
  Serial.print("{\"sensorDigital\": ");
  Serial.print(sensorDigital);
  Serial.print(", ");

  Serial.print("\"sensorAnalog\": ");
  Serial.print(sensorAnalog);
  Serial.println("}");
}

void loop()
{
  int digital = readSensorDigital();
  int analog = readSensorAnalog();
  sendData(digital, analog);
}