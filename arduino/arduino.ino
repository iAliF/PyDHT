#include "TimeLib.h"
#include "DHT.h"


#define PIN 7       // Sensor data pin
#define TYPE DHT11  // Sensor Type (DHT11, DHT12, DHT21, DHT22, AM2301)
#define BAUD 9600   // Serial baud

DHT dht(PIN, TYPE);

void setup() {
  Serial.begin(BAUD);
  dht.begin();
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // Sync the time if it's not
  if (Serial.available() && timeStatus() != timeSet) {
    processSyncMessage();
    return ;
  }

  // Read data from sensor
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Check if data is received or not
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("None");
    return;
  }

  // Compute the heat index
  float heatIndex = dht.computeHeatIndex(temperature, humidity, false);


  // Write data to the Serial port
  Serial.print(now());
  Serial.print("|");
  Serial.print(temperature);
  Serial.print("|");
  Serial.print(humidity);
  Serial.print("|");
  Serial.println(heatIndex);

  // Wait a second
  delay(1000);
}

// From TimeLib example (Edited)
void processSyncMessage() {
  unsigned long pcTime;
  const unsigned long DEFAULT_TIME = 1357041600;  // Jan 1 2013

  if (Serial.find("TIME")) {
    pcTime = Serial.parseInt();
    if (pcTime >= DEFAULT_TIME) {  // check the integer is a valid time (greater than Jan 1 2013)
      setTime(pcTime);             // Sync Arduino clock to the time received on the serial port
      Serial.println("SYNCED");
      digitalWrite(LED_BUILTIN, HIGH);
    }
  }
}