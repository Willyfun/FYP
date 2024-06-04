#include <WiFi.h>
#include "ThingSpeak.h"
#define Offline_pin 15
#define Online_pin 4
#define RXp2 16
#define TXp2 17
#define channel_ID 2175178
#define channel_APIKEY "ME32UIN16WFW4VNT"
// Replace with your network credentials (STATION)
const char* ssid = "POCOF3";
const char* password = "02090816";
const char* server = "api.thingspeak.com";

WiFiClient client;

bool handshakeComplete = false; // Flag to indicate handshake completion

void initWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    digitalWrite(Offline_pin, HIGH);
    delay(1000);
  }
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, RXp2, TXp2);
  pinMode(Offline_pin, OUTPUT);
  pinMode(Online_pin, OUTPUT);
  initWiFi();
  Serial.print("RRSI: ");
  Serial.println(WiFi.RSSI());
  ThingSpeak.begin(client);
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    digitalWrite(Offline_pin, LOW);
    digitalWrite(Online_pin, HIGH);
  }

  if (!handshakeComplete) {
    Serial2.println("Ready"); // Send a message to indicate readiness
    delay(100); // Allow time for the message to be transmitted

    if (Serial2.available()) {
      String response = Serial2.readStringUntil('\n');
      response.trim();
      if (response == "OK") {
        handshakeComplete = true; // Set the handshake flag
      }
    }
  } else {
    float pulseValue = readPulseValue();
    float tempValue = readTempValue();
    Serial.println(pulseValue);
    Serial.println(tempValue);
    ThingSpeak.writeField(channel_ID, 1,tempValue, channel_APIKEY);
    delay(15000);
    ThingSpeak.writeField(channel_ID, 2,pulseValue, channel_APIKEY);
    delay(15000);
    // Rest of the code for sending data to Thingspeak
  }

  delay(800);
}

float readPulseValue() {
  String message;

  while (Serial2.available()) {
    char c = Serial2.read();
    message += c;
    if (c == '\n') {
      break;
    }
    delay(10);
  }

  int startIdx = message.indexOf("BPM = ") + 6;
  int endIdx = message.indexOf('\n', startIdx);
  String pulseString = message.substring(startIdx, endIdx);

  float pulseValue = pulseString.toFloat();

  Serial.print("Pulse value received from Arduino: ");
  Serial.println(pulseValue);

  return pulseValue;
}

float readTempValue() {
  String message;

  while (Serial2.available()) {
    char c = Serial2.read();
    message += c;
    if (c == '\n') {
      break;
    }
    delay(10);
  }

  int startIdx = message.indexOf("Temperature =") + 13;
  int endIdx = message.indexOf('*', startIdx);
  String tempString = message.substring(startIdx, endIdx);

  float tempValue = tempString.toFloat();

  Serial.print("Temperature value received from Arduino: ");
  Serial.println(tempValue);

  return tempValue;
}
