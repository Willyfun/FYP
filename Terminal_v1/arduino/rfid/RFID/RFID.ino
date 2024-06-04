#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create an instance of the MFRC522 class

void setup() {
  Serial.begin(9600);  // Initialize serial communication
  SPI.begin();         // Initialize SPI communication
  mfrc522.PCD_Init();  // Initialize the MFRC522 RFID module

  Serial.println("RFID Reader Initialized");
}

void loop() {
  // Check if a new card is present
  if (mfrc522.PICC_IsNewCardPresent()) {
    // Read the card's UID
    if (mfrc522.PICC_ReadCardSerial()) {
      String uid = "";
      for (byte i = 0; i < mfrc522.uid.size; i++) {
        uid += String(mfrc522.uid.uidByte[i], HEX);
      }
      Serial.println("RFID Tag Detected: " + uid);
      Serial.flush();
    }
    delay(1000);  // Wait for a short duration before detecting the next tag
  }
}
