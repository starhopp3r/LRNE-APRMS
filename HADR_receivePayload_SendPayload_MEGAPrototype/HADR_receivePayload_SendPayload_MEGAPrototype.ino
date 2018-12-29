// LoPy placeholder: Arduino MEGA
// LoPy receive code (Read on Arduino MEGA Serial Port)
// Prototype mathod: Handset ==> Arduino UNO
// LoPy ==> Arduino MEGA

/*JSON object SEND from handset
   {
    "user":"",
    "latitude":"",
    "longitude:""
   }
*/

String payloadHandset = "";
String broadcastMsg = "SudoX is on the way!";
float flat = 0.2359;
float flon = 104.56;
unsigned long screenTime = millis();

// ==============================Some parser codes==============================
String parseMessageLoPy(String rawMessage, byte index) {
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
String encodeMessageHandset(String message) {
  // NOTE: USER will not send back broadcast message!!!
  String buffer = "{";
  buffer += "\"user\":\"" + message + "\",";
  buffer += "\"latitude\":\"" + String(flat) + "\",";
  buffer += "\"longitude\":\"" + String(flon) + "\"";
  buffer += "}";
  return buffer;
}

String parseMessageHandset(String rawMessage, byte index) {
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
    ind = rawMessage.indexOf("broadcast");
    ind += 9;
  }
  ind += 3;
  return String(rawMessage.substring(ind, rawMessage.indexOf('"', ind)));
}
//======================================end===============================

//SoftwareSerial handset (11,10);

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600); // Handset Serial 
  Serial2.begin(9600); // LoPy Serial

  Serial1.print("ready!");
  //Step 0: LoPy waits for Arduino to be ready, then sends the previous state and broadcast message
  //        This case we assume it is Shelter
  while (true){
    if (Serial1.available()&&Serial2.available()){
      Serial.println("Both are ready!");
      break;
    }else if(!Serial1.available()&&Serial2.available()){
      Serial.println("Handset not ready, LoPy ready");
      Serial2.println("OK!");
    }else if(Serial1.available()&&!Serial2.available()){
      Serial.println("Handset ready, LoPy not ready");
    }else if(!Serial1.available()&&!Serial2.available()){
      Serial.println("Both not ready!");
    }
  }
  Serial2.print("{\"user\":"); Serial2.print("\"Shelter\",");
  Serial2.print("\"broadcast\":\""); Serial2.print(broadcastMsg);Serial2.print("\"}");
  Serial.println("LoPy has sent information to Handset! \n");
  
  //Step 1: Upon boot from Arduino, reads from LoPy for previous state and broadcast message
  //while(Serial2.available()){
    payloadHandset = Serial1.readString();
    Serial.println(payloadHandset);
  //}
  Serial.println("This is the message received from LoPy:");
  Serial.print("\"user\":\"");Serial.print(parseMessageHandset(payloadHandset, 0));Serial.println('\"');
  Serial.print("\"broadcast\":\"");Serial.print(parseMessageHandset(payloadHandset,1));Serial.println('\"');
}

void loop() {
  // Looping: Every 5 seconds, Handset will send payload, then wait for loPy to read
  //          Then, LoPy will read, repeat
  while ((millis() - screenTime) >5000){
  String payloadToLoPy = encodeMessageHandset("Shelter");
  String payloadFromHandset = "";
  
  Serial1.println(payloadToLoPy);
  Serial.print("Payload sent from Handset to LoPy:");Serial.println(payloadToLoPy);
  while(!Serial2.available());
  while(Serial2.available()){
    payloadFromHandset = Serial2.readString();
  }
  Serial.print("This is the message from handset: ");Serial.println(payloadFromHandset);
  Serial.println("Parsing...");
  Serial.print("user:      "); Serial.println(parseMessageLoPy(payloadFromHandset, 0));
  Serial.print("latitude:  "); Serial.println(parseMessageLoPy(payloadFromHandset, 1));
  Serial.print("longitude: "); Serial.println(parseMessageLoPy(payloadFromHandset, 2));
  screenTime = millis();}

}


