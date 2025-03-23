// Hall sensor pins
const int digitalPin = 12; // linear Hall magnetic sensor digital interface
const int analogPin = A0;  // linear Hall magnetic sensor analog interface

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
  int digital = digitalRead(digitalPin);
  int analog = analogRead(analogPin);
  sendData(digital, analog);
}