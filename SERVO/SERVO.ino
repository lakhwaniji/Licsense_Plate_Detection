
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Servo.h>

const char* ssid = "GALAXYA51";
const char* password = "love@2000";
const char* mqtt_server = "192.168.238.13";

WiFiClient espClient;
PubSubClient client(espClient);
Servo myservo;
const int servoPin = 5;

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  payload[length] = '\0'; // Null-terminate the payload
  String receivedMessage = String((char*)payload);

  Serial.print("Received message on topic: ");
  Serial.println(topic);
  Serial.print("Received message: ");
  Serial.println(receivedMessage);
  int angle = receivedMessage.toInt();
  myservo.write(angle);
  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  } else {
    digitalWrite(BUILTIN_LED, HIGH);  // Turn the LED off by making the voltage HIGH
  }

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266";
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("ESP8266", "Love");
      client.subscribe("servo");
      // ... and resubscribe
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(2000);
    }
  }
}

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  myservo.attach(servoPin);
  myservo.write(0);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}

