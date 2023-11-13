#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define SS_PIN D4  // Pin connected to SDA of MFRC522
#define RST_PIN D3 // Pin connected to RST of MFRC522
#define LED_PIN D2 // Pin connected to an LED for indication

const char* ssid = "GALAXYA51";
const char* password = "love@2000";
const char* mqtt_server = "192.168.238.13";

WiFiClient espClient;
PubSubClient client(espClient);

MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance

bool startRFIDScan = false;

void callback(char* topic, byte* payload, unsigned int length) {
  // Handle incoming message on subscribed topic
  payload[length] = '\0'; // Null-terminate the payload
  String receivedTopic = String(topic);
  String receivedMessage = String((char*)payload);

  Serial.print("Received message on topic: ");
  Serial.println(receivedTopic);
  
  // Check if the received message is the trigger message
  if (receivedTopic.equals("start_rfid_scan") && receivedMessage.equals("start")) {
    startRFIDScan = true;
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Connect to MQTT
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect("NodeMCU")) {
      Serial.println("Connected to MQTT");
      client.subscribe("start_rfid_scan"); // Subscribe to the topic to start RFID scan
    } else {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" Retrying in 5 seconds...");
      delay(5000);
    }
  }

  // Initialize RFID reader
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("RFID reader initialized");
}

void loop() {
  if (client.connected()) {
    // Check for MQTT messages
    client.loop();

    // Check for RFID card if startRFIDScan flag is true
    if (startRFIDScan) {
      if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
        String uid = "";
        for (byte i = 0; i < mfrc522.uid.size; i++) {
          uid += String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
          uid += String(mfrc522.uid.uidByte[i], HEX);
        }
        uid.toUpperCase();

        // Publish UID to MQTT topic
        client.publish("authentic", uid.c_str());

        Serial.println("Card UID: " + uid);
        digitalWrite(LED_PIN, HIGH);
        delay(3000);
        digitalWrite(LED_PIN, LOW);
        
        // Reset the flag after RFID scan
        startRFIDScan = false;
      }
    }
  } else {
    // Reconnect to MQTT if connection is lost
    if (!client.connected()) {
      Serial.println("Lost MQTT connection. Reconnecting...");
      if (client.connect("NodeMCU")) {
        Serial.println("Reconnected to MQTT");
        client.subscribe("start_rfid_scan"); // Subscribe to the topic to start RFID scan
      } else {
        Serial.print("Failed, rc=");
        Serial.print(client.state());
        Serial.println(" Retrying in 5 seconds...");
        delay(5000);
      }
    }
  }
}
