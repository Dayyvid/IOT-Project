#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi/MQTT parameters
#define WLAN_SSID       "WLAN_SSID"
#define WLAN_PASS       "WLAN_PASS"
#define BROKER_IP       "BROKER_IP "

// vars
#define LED D0
#define BUTTON D2
#define ON 0
#define OFF 1

bool buttonState;
bool securitySystemState;
bool previousState;

WiFiClient client;
PubSubClient mqttclient(client);

void callback (char* topic, byte* payload, unsigned int length) {
  // add null terminator to end of message
  payload[length] = '\0';

  Serial.write(payload, length); //print incoming messages
  Serial.write("\n");

  // if message tells arduino to turn on light
  if((strcmp((char*)(payload), "arduinoLedOn")) == 0){
    digitalWrite(LED, HIGH);
  }
}


void setup() {
  // setup pin as output
  pinMode(LED, OUTPUT);
  pinMode(BUTTON, INPUT);
  
  securitySystemState = OFF;
  previousState = OFF;

  // connect to output channel
  Serial.begin(115200);

  // connect to wifi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print("Trying to connect to WiFi\n");
  }

  // print wifi info
  Serial.println(F("WiFi connected"));

  // connect to mqtt server
  mqttclient.setServer(BROKER_IP, 1883);
  mqttclient.setCallback(callback);
  connect();

  // set up LED
  digitalWrite(LED, LOW);
}

void loop() {

  if (!mqttclient.connected()) { //make sure mqqt is connected
    connect();
  }
  mqttclient.loop(); // run client
  
  // get button state
  buttonState = digitalRead(BUTTON);
  if(buttonState == ON and buttonState != previousState) {
    if(securitySystemState == OFF) {
      mqttclient.publish("/fromArduino", "securitySystemOn", false);
      securitySystemState = ON;
      digitalWrite(LED, LOW);
      Serial.print("Sent on message\n");
    } else {
      mqttclient.publish("/fromArduino", "securitySystemOff", false);
      securitySystemState = OFF;
      Serial.print("Sent off message\n");
    }
  }
  previousState = buttonState;
  delay(100);
}

// connect to mqtt
void connect() {
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println(F("Wifi issue"));
    delay(3000);
  }
  Serial.print(F("Connecting to MQTT server... "));
  while(!mqttclient.connected()) {
    if (mqttclient.connect(WiFi.macAddress().c_str())) {
      Serial.println(F("MQTT server Connected!"));
      mqttclient.subscribe("/fromRPi"); // subscribe to fromRPi channel   
    } else {
      Serial.print(F("MQTT server connection failed! rc="));
      Serial.print(mqttclient.state());
      Serial.println("try again in 10 seconds");
      // Wait 5 seconds before retrying
      delay(20000);
    }
  }
}
