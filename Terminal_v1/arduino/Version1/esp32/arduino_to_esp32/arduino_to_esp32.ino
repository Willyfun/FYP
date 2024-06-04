#include <WiFi.h>
#define Offline_pin 15
#define Online_pin 4
#define RXp2 16
#define TXp2 17

// Replace with your network credentials (STATION)
const char* ssid = "POCOF3";
const char* password = "02090816";
const char* server = "api.thingspeak.com";
String apiKey = "ME32UIN16WFW4VNT";

WiFiClient client;
//String message;

//volatile bool newDataAvailable = false; // Flag to indicate new data is available

/*void IRAM_ATTR serialISR() {
  while (Serial2.available()) {
    char c = Serial2.read();
    message += c;
  }
  newDataAvailable = true; // Set the flag to indicate new data is available
}*/

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

  //attachInterrupt(digitalPinToInterrupt(RXp2), serialISR, FALLING);
}

void loop() {
  if(WiFi.status() == WL_CONNECTED){
    digitalWrite(Offline_pin, LOW);
    digitalWrite(Online_pin, HIGH);
  }
  //Serial.println("Message Received: ");
  //Serial.println(Serial2.readString());
  //if(newDataAvailable){

    //newDataAvailable = false;
  
    float pulseValue = readPulseValue();
    float tempValue = readTempValue();
    Serial.println(pulseValue);
    Serial.println(tempValue);
  //}
  //Serial.println(pulseValue);
  //Serial.println(tempValue);

  /*if (client.connect(server,80))   //   "184.106.153.149" or api.thingspeak.com
  {  
    String postStr = apiKey;
    postStr +="&field1=";
    postStr += String(tempValue);
    postStr +="&field2=";
    postStr += String(pulseValue);
    postStr += "\r\n\r\n";
    client.print("POST /update HTTP/1.1\n");
    client.print("Host: api.thingspeak.com\n");
    client.print("Connection: close\n");
    client.print("X-THINGSPEAKAPIKEY: "+apiKey+"\n");
    client.print("Content-Type: application/x-www-form-urlencoded\n");
    client.print("Content-Length: ");
    client.print(postStr.length());
    client.print("\n\n");
    client.print(postStr);
 
    Serial.print("Temperature: ");
    Serial.print(tempValue);
    Serial.print("BPM: ");
    Serial.print(pulseValue);
    Serial.println("%. Send to Thingspeak.");
  }
  client.stop();
 
  Serial.println("Waiting...");
  
  // thingspeak needs minimum 15 sec delay between updates
  delay(1000);*/
}

float readPulseValue() {
  String message;

  while (Serial2.available()) {
    char c = Serial2.read();
    message += c;
    if (c == '\n') { // Check for the termination character
      break;
    }
    delay(10); // Adjust the delay as needed
  }

  // Rest of the code remains the same
}

float readTempValue() {
  String message;

  while (Serial2.available()) {
    char c = Serial2.read();
    message += c;
    if (c == '\n') { // Check for the termination character
      break;
    }
    delay(10); // Adjust the delay as needed
  }

  // Rest of the code remains the same
}





/*float readPulseValue() {
  // Read the pulse value from Arduino
  String message;

  while (Serial2.available()) {
    char c = Serial2.read();
    message += c;
    delay(100);
  }

  int startIdx = message.indexOf("BPM = ") + 6; // Find the start index of the pulse value
  int endIdx = message.indexOf('\n', startIdx); // Find the end index of the pulse value
  String pulseString = message.substring(startIdx, endIdx);

  float pulseValue = pulseString.toFloat();

  Serial.print("Pulse value received from Arduino: ");
  Serial.println(pulseValue);

  return pulseValue;
}

float readTempValue() {
  // Read the temperature value from Arduino
  String message;

  while (Serial2.available()) {
    char c = Serial2.read();
    message += c;
    delay(100);
  }

  int startIdx = message.indexOf("Temperature =") + 13; // Find the start index of the temperature value
  int endIdx = message.indexOf('*', startIdx); // Find the end index of the temperature value
  String tempString = message.substring(startIdx, endIdx);

  float tempValue = tempString.toFloat();

  Serial.print("Temperature value received from Arduino: ");
  Serial.println(tempValue);

  return tempValue;
}*/