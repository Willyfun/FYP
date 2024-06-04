#define BLYNK_TEMPLATE_ID "TMPL6RS92fdyE"
#define BLYNK_TEMPLATE_NAME "Temperature and Pulse Sensor"
#define BLYNK_AUTH_TOKEN "EBJCId4V25rcLjcrh4JMKBWIG2dDBO5v"
#define BLYNK_PORT 80
#define VIRTUAL_TEMP_PIN V0
#define VIRTUAL_PULSE_PIN V1

#include <WiFi.h>
#include <BlynkSimpleEsp32.h>

#define Offline_pin 15
#define Online_pin 4
#define RXp2 16
#define TXp2 17

// Replace with your network credentials (STATION)
const char* ssid = "POCOF3";
const char* password = "02090816";
const char* server = "blynk.cloud";

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
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, password, server, BLYNK_PORT);
  Serial.print("RRSI: ");
  Serial.println(WiFi.RSSI());
}

void loop() {
  Blynk.run();
  if (WiFi.status() == WL_CONNECTED) {
    digitalWrite(Offline_pin, LOW);
    digitalWrite(Online_pin, HIGH);
  }

  if (!handshakeComplete) {
    send_ready_signal_to_arduino(); // Send ready signal to Arduino
    check_handshake_ack(); // Check for handshake acknowledgement from Arduino
  } else {
    // Rest of the code, data processing or transmission, if any
    float pulseValue = readPulseValue();
    float tempValue = readTempValue();

    Blynk.virtualWrite(VIRTUAL_TEMP_PIN, tempValue);
    Blynk.virtualWrite(VIRTUAL_PULSE_PIN, pulseValue);

    send_handshake_ack(); // Send handshake acknowledgement to Arduino
  }

  delay(1000);
}

void send_ready_signal_to_arduino() {
  Serial2.println("Ready"); // Send ready signal to Arduino
}

void check_handshake_ack() {
  if (Serial2.available()) {
    String message = Serial2.readStringUntil('\n');
    message.trim();
    if (message == "READY") {
      handshakeComplete = true; // Set the handshake flag
    }
  }
}

void send_handshake_ack() {
  Serial2.println("ACK"); // Send handshake acknowledgement to Arduino
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

  int startIdx = message.indexOf("Temperature = ") + 14;
  int endIdx = message.indexOf('*', startIdx);
  String tempString = message.substring(startIdx, endIdx);

  float tempValue = tempString.toFloat();

  Serial.print("Temperature value received from Arduino: ");
  Serial.println(tempValue);

  return tempValue;
}
