/* ------------------------------------------------- */

#include <Arduino.h>
#include "ESPTelnet.h"
#include "X9C103P.h"

/* ------------------------------------------------- */

#ifdef ESP32
  #include <WiFi.h>
  #include <AsyncTCP.h>
#else
  #include <ESP8266WiFi.h>
  #include <ESPAsyncTCP.h>
#endif
#include <ESPAsyncWebServer.h>

/* ------------------------------------------------- */

AsyncWebServer server(80);

/* ------------------------------------------------- */

const char* ssid     = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

const char* PARAM_INPUT_1 = "idInput1";

int inputSWSerialTransmitted;

/* ------------------------------------------------- */

// HTML web page to handle 1 input field (idInput1)
const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML><html><head>
  <title>Webserver Input Form</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  </head><body>
  <form action="/get">
    Input1: <input type="text" name="idInput1">
    <input type="submit" name="idSubmit" value="Submit">
  </form>
</body></html>)rawliteral";

void notFound(AsyncWebServerRequest *request) {
  request->send(404, "text/plain", "Not found");
}

/* ------------------House IP Address --------------- */

// Set your Static IP address
IPAddress local_IP(192, 168, 0, 184);
// Set your Gateway IP address
IPAddress gateway(192, 168, 0, 1);

/* ------------------ Firm IP Address --------------- */

//// Set your Static IP address
//IPAddress local_IP(10, 5, 4, 100);
//// Set your Gateway IP address
//IPAddress gateway(10, 5, 4, 1);

// Set your Mask address
IPAddress subnet(255, 255, 255, 0);
// Set your DNS address
IPAddress primaryDNS(8, 8, 8, 8);   //optional
IPAddress secondaryDNS(8, 8, 4, 4); //optional

ESPTelnet telnet;
uint16_t  port = 23;
WiFiServer TelnetServer(port);
WiFiClient Telnet;

const float V_REF = 5.; // Change if using different Vref
const int UP = 0;
const int DOWN = 1;

float voltage = 0;
int i, j, e, f;
float Volt;
int U;


/* -----------------TELNET----------------------- */

void setupSerial(long speed, String msg = "") {
  Serial.begin(speed);
  while (!Serial) {
  }
  delay(200);  
  Serial.println();
  Serial.println();
  if (msg != "") Serial.println(msg);
}

/* ------------------------------------------------- */

bool isConnected() {
  return (WiFi.status() == WL_CONNECTED);
}

/* ------------------------------------------------- */

bool connectToWiFi(const char* ssid, const char* password, int max_tries = 20, int pause = 500) {
  int i = 0;
  WiFi.mode(WIFI_STA);
  #if defined(ARDUINO_ARCH_ESP8266)
    WiFi.forceSleepWake();
    delay(200);
  #endif
  WiFi.begin(ssid, password);
  do {
    delay(pause);
    Serial.print(".");
  } while (!isConnected() || i++ < max_tries);
  WiFi.setAutoReconnect(true);
  WiFi.persistent(true);
  return isConnected();
}

/* ------------------------------------------------- */

void errorMsg(String error, bool restart = true) {
  Serial.println(error);
  if (restart) {
    Serial.println("Rebooting now...");
    delay(2000);
    ESP.restart();
    delay(2000);
  }
}

/* ------------------------------------------------- */

void setupTelnet() {  
  // passing on functions for various telnet events
  telnet.onConnect(onTelnetConnect);
  telnet.onConnectionAttempt(onTelnetConnectionAttempt);
  telnet.onReconnect(onTelnetReconnect);
  telnet.onDisconnect(onTelnetDisconnect);
  
  // passing a lambda function
  telnet.onInputReceived([](String str) {
    Serial.print(str);
  });

  telnet.setLineMode(false);
  Serial.print("- Telnet Line Mode: "); Serial.println(telnet.isLineModeSet() ? "YES" : "NO");
  
  Serial.print("- Telnet: ");
  if (telnet.begin(port)) {
    Serial.println("running");
  } else {
    Serial.println("error.");
    errorMsg("Will reboot...");
  }
}

/* ------------------------------------------------- */

// (optional) callback functions for telnet events
void onTelnetConnect(String ip) {
  Serial.print("- Telnet: ");
  Serial.print(ip);
  Serial.println(" connected");
  telnet.println("\nWelcome " + telnet.getIP());
  telnet.println("(Use ^] to disconnect.)");
}

void onTelnetDisconnect(String ip) {
  Serial.print("- Telnet: ");
  Serial.print(ip);
  Serial.println(" disconnected");
}

void onTelnetReconnect(String ip) {
  Serial.print("- Telnet: ");
  Serial.print(ip);
  Serial.println(" reconnected");
}

void onTelnetConnectionAttempt(String ip) {
  Serial.print("- Telnet: ");
  Serial.print(ip);
  Serial.println(" tried to connected");
}

void handleTelnet() {
  if (TelnetServer.hasClient()) {
    if (!Telnet || !Telnet.connected()) {
      if (Telnet) Telnet.stop();
      Telnet = TelnetServer.available();
    } else {
      TelnetServer.available().stop();
    }
  }
}

void telnetRun(){
  handleTelnet();
  // using Telnet to check whether temperature input is transmitted
  Telnet.print("Temperature : ");
  Telnet.print(inputSWSerialTransmitted);
  Telnet.print(" <=> Voltage : ");
  Telnet.print(10 * inputSWSerialTransmitted + 500);
  Telnet.println();
  delay(300);
}

//===============================================================================
//  Subroutine to move the wiper UP or DOWNVoltage
//===============================================================================
void Move_Wiper(int direction) {
    switch (direction) {
    case UP:
        digitalWrite(UD_PIN, HIGH);
        delayMicroseconds(5); // Set to increment
        digitalWrite(INC_PIN, LOW);
        delayMicroseconds(5); // Pulse INC pin low
        digitalWrite(INC_PIN, HIGH);
        break;
    case DOWN:
        digitalWrite(UD_PIN, LOW);
        delayMicroseconds(5); // Set to decrement
        digitalWrite(INC_PIN, LOW);
        delayMicroseconds(5); // Pulse INC pin low
        digitalWrite(INC_PIN, HIGH);
        break;
    default:
        break;
    }
}
void Move_Wiper0(int direction) {
    switch (direction) {
    case UP:
        digitalWrite(UD0_PIN, HIGH);
        delayMicroseconds(5); // Set to increment
        digitalWrite(INC0_PIN, LOW);
        delayMicroseconds(5);
        digitalWrite(INC0_PIN, HIGH);
        break;
    case DOWN:
        digitalWrite(UD0_PIN, LOW);
        delayMicroseconds(5); // Set to decrement
        digitalWrite(INC0_PIN, LOW);
        delayMicroseconds(5); // Pulse INC pin low
        digitalWrite(INC0_PIN, HIGH);
        break;
    default:
        break;
    }
}
//===============================================================================
//  Subroutine to handle characters typed via Serial Monitor Window
//===============================================================================
void DoSerial() {
    i = 0;
    j = 0;
    e = 0;
    f = 0;
    String ch = Serial.readString();

    // Read the character we received
    Volt = (10 * ch.toFloat() + 500); //temp to voltage
    U = round(Volt);
    int d = 100 - (U % 100); //steps float
    int b = ((U / 100) + 1) * 3;

    // Decrement setting

    while (j < 150) {
        j++;
        Move_Wiper(DOWN);
    }
    while (i < b) {
        i++;
        Move_Wiper(UP);
    }

    while (f < 150) {
        f++;
        Move_Wiper0(DOWN);
    }
    while (e < d) {
        e++;
        Move_Wiper0(UP);
    }
}
//===============================================================================
//  Initialization
//===============================================================================
void setup() {
    Serial.begin(9600);
    pinMode(CS_PIN, OUTPUT);
    pinMode(UD_PIN, OUTPUT);
    pinMode(INC_PIN, OUTPUT);
    pinMode(CS0_PIN, OUTPUT);
    pinMode(UD0_PIN, OUTPUT);
    pinMode(INC0_PIN, OUTPUT);

    digitalWrite(INC_PIN, HIGH);
    digitalWrite(CS_PIN, LOW);
    digitalWrite(INC0_PIN, HIGH);
    digitalWrite(CS0_PIN, LOW); // Enable the X9C103P chip
    // Print X9C103P power up value

    // Configures static IP address
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
    Serial.println("STA Failed to configure");
  }
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
  delay(1000);
  Serial.println("Connecting to WiFi..");
  }
  //start UART and the server
  TelnetServer.begin();
  TelnetServer.setNoDelay(true); 
  
  Serial.print("Ready! Use 'telnet ");
  Serial.println();
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.println();
  Serial.print("- Telnet: "); Serial.print(WiFi.localIP()); Serial.print(" "); Serial.println(port);
  setupTelnet();

  // Send web page with input fields to client
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/html", index_html);
  });

  // Send a GET request to <ESP_IP>/get?idInput1=<inputMessage>
  server.on("/get", HTTP_GET, [] (AsyncWebServerRequest *request) {
    String inputMessage;
    String inputParam;
    // GET idInput1 value on <ESP_IP>/get?idInput1=<inputMessage>
    if (request->hasParam(PARAM_INPUT_1)) {
      inputMessage = request->getParam(PARAM_INPUT_1)->value();
      inputParam = PARAM_INPUT_1;
      inputSWSerialTransmitted = inputMessage.toInt();
    }
    else {
      inputMessage = "No message sent";
      inputParam = "none";
    }
    Serial.println(inputMessage);
    request->send(200, "text/html", "HTTP GET request sent to your ESP on input field (" 
                                     + inputParam + ") with value: " + inputMessage +
                                     "<br><a href=\"/\">Return to Home Page</a>");
  });
  server.onNotFound(notFound);
  server.begin();
}
//===============================================================================
//  Main
//===============================================================================
void loop() {
    telnetRun();
    if (Serial.available()) DoSerial(); // Just loop looking for user input
}
