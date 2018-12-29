// LoPy placeholder: Arduino MEGA
// LoPy receive code
#include <SoftwareSerial.h>

/*JSON object SEND from handset
   {
    "user":"",
    "latitude":"",
    "longitude:""
   }
*/

// ==============================Some parser codes==============================
String parseMessage(String rawMessage, byte index) {
  if (rawMessage.substring("{") != 0) {
    Serial.println(rawMessage);
    return "Object is not json!";
  }
  byte ind;
  if (index == 0) {
    ind = rawMessage.indexOf("user");
    ind += 4;
  }
  else if (index == 1) {
    ind = rawMessage.indexOf("latitude");
    ind += 8;
  }
  else if (index == 2) {
    ind = rawMessage.indexOf("longitude");
    ind += 9;
  }
  ind += 3;
  return String(rawMessage.substring(ind, rawMessage.indexOf('"', ind)));
}
//======================================end===============================

SoftwareSerial handset (11,10);
String payload;
void setup() {
  Serial.begin(9600);
  handset.begin(9600); 
}

void loop() {
  payload = "";
  handset.println(payload);
  handset.listen();
  while(handset.available()){
    char c = handset.read();
    payload += c;
  }
  Serial.println(payload);
  Serial.print("user:      ");Serial.println(parseMessage(payload,0));
  Serial.print("latitude:  ");Serial.println(parseMessage(payload,1));
  Serial.print("longitude: ");Serial.println(parseMessage(payload,2));
  delay(2000);

}


