#include <SoftwareSerial.h>

const int rxPin = 10;
const int txPin = 11;

const int digitalPin = 12; // linear Hall magnetic sensor digital interface
const int analogPin = A0;  // linear Hall magnetic sensor analog interface

const byte START_BYTE = 0x0A;
const byte END_BYTE = 0x0B;
const int DATA_SIZE = 4;

// Set up a new SoftwareSerial object
SoftwareSerial mySerial(rxPin, -1);

void setup()
{
  pinMode(digitalPin, INPUT);
  pinMode(analogPin, INPUT);
  Serial.begin(9600);

  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);

  // Set the baud rate for the SoftwareSerial object
  mySerial.begin(9600);
}

void test()
{
  while (mySerial.available())
  {
    byte data = mySerial.read();
    Serial.println(data, "HEX");
  }
}

int readSensorAnalog()
{
  return analogRead(digitalPin);
}
int readSensorDigital()
{
  return digitalRead(digitalPin);
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