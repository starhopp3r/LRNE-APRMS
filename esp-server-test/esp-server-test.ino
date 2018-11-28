#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
 
void setup() {
  // Serial connection
  Serial.begin(115200);
  // Credentials for WiFi connection
  WiFi.begin("xxxxx", "xxxxx");

  // Wait for the WiFI connection completion
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Waiting for connection");
  }
}
 
void loop() {
  // Check WiFi connection status
  if (WiFi.status() == WL_CONNECTED) {
    // Declaring static JSON buffer
    StaticJsonBuffer<300> JSONbuffer;
    JsonObject& JSONencoder = JSONbuffer.createObject(); 
 
    JSONencoder["sensorType"] = "Temperature";
 
    JsonArray& values = JSONencoder.createNestedArray("values"); //JSON array
    values.add(20); //Add value to array
    values.add(21); //Add value to array
    values.add(23); //Add value to array
 
    JsonArray& timestamps = JSONencoder.createNestedArray("timestamps"); //JSON array
    timestamps.add("10:10"); //Add value to array
    timestamps.add("10:20"); //Add value to array
    timestamps.add("10:30"); //Add value to array
 
    char JSONmessageBuffer[300];
    JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
    Serial.println(JSONmessageBuffer);

    // Declare object of class HTTPClient
    HTTPClient http;

    // Specify request destination
    http.begin("http://local-ip-address:5000/dev");
    // Specify content-type header
    http.addHeader("Content-Type", "application/json");
    // Send the request
    int httpCode = http.POST(JSONmessageBuffer);
    // Get the response payload
    String payload = http.getString();
    // Print HTTP return code
    Serial.println(httpCode);
    // Print request response payload
    Serial.println(payload);

    // Close connection
    http.end();
  } else {
    Serial.println("Error in WiFi connection");
  }

  // Send a request every 30 seconds
  delay(30000);
}

