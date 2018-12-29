// Handset sending code
#include <SoftwareSerial.h>

SoftwareSerial loPy(13,12);
unsigned long screenTime = millis();
float flat = 0;
float flon = 0;
String payload = "";

// ==============================Some parser codes==============================
String encodeMessage(String message) {
  // NOTE: USER will not send back broadcast message!!!
  String buffer = "{";
  buffer += "\"user\":\"" + message + "\"";
  buffer += "\"latitude\"" + String(flat) + "\",";
  buffer += "\"longitude\"" + String(flon) + "\"";
  buffer += "}";
  return buffer;
}
//======================================end===============================

void setup() {
  Serial.begin(9600);
  loPy.begin(9600);
  Serial.println("Ready!");
  while(!loPy.available());
  loPy.listen();
  /*while(loPy.available()){
    char c = loPy.read();
    payload += c;
  }
  Serial.println(payload);
  Serial.print("user: ");Serial.println(parseMessage(payload,0));
  Serial.print("broadcast: ");Serial.println(parseMessage(payload,1));
  delay(2000);*///suspect arduino has some limitations for reading and writing form the same port
}

void loop() {
  // put your main code here, to run repeatedly:
  while (!((millis() - screenTime) > 5000)); //waits every 5 seconds
  loPy.print(encodeMessage("Shelter"));
}
