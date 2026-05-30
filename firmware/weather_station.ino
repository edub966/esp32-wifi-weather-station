#include "DHT.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>


const char* ssid      = "YOUR WIFI NETWORK NAME";
const char* password  = "YOUR WIFI PASSWORD";
const char* serverUrl = "http://YOUR_IP_ADDRESS/readings";


#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();

  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected! ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    float humidity = dht.readHumidity();
    float tempC    = dht.readTemperature();
    float tempF    = dht.readTemperature(true);

    if (isnan(humidity) || isnan(tempC)) {
      Serial.println("Failed to read from DHT22!");
      delay(5000);
      return;
    }

    int   rssi         = WiFi.RSSI();
    float vcc          = analogReadMilliVolts(34) / 1000.0; // 3.3V rail approximation
    long  uptime_secs  = millis() / 1000;

    Serial.print("Sending — ");
    Serial.print(tempF);
    Serial.print("°F, ");
    Serial.print(humidity);
    Serial.print("% RH, RSSI: ");
    Serial.println(rssi);

    StaticJsonDocument<300> doc;
    doc["temperature_c"] = tempC;
    doc["temperature_f"] = tempF;
    doc["humidity"]      = humidity;
    doc["rssi"]          = rssi;
    doc["vcc"]           = 3.3;       
    doc["uptime"]        = uptime_secs;

    String jsonString;
    serializeJson(doc, jsonString);

    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    int responseCode = http.POST(jsonString);
    Serial.print("Server response: ");
    Serial.println(responseCode);
    http.end();
  }

  delay(300000);
}