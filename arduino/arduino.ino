#include "DHT.h"


#define PIN 7       // Sensor data pin
#define TYPE DHT11  // Sensor Type (DHT11, DHT12, DHT21, DHT22, AM2301)
#define BAUD 9600   // Serial baud

DHT dht(PIN, TYPE);

void setup() {
  Serial.begin(BAUD);
  dht.begin();
}

void loop() {
  // Wait a few seconds
  delay(500);

  // Read data
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Check if data is received or not
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("None");
    return;
  }

  float heatIndex = dht.computeHeatIndex(temperature, humidity, false);

  Serial.print(temperature);
  Serial.print("|");
  Serial.print(humidity);
  Serial.print("|");
  Serial.println(heatIndex);
}