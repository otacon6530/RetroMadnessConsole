#include <ArduinoJson.h>
int analogPin = A0; 
int insertPin = 3;
int gameID = 0;  // variable to store the value read
String description= "Retro Madness Cartridge Reader v0.2";
int state = 0;
int insertState = 0;

void setup(void) {
  pinMode(analogPin, INPUT);//floppy resistance to determin game id.
  pinMode(insertPin, INPUT);//Is floppy in drive?
  Serial.begin(115200);
};

//command parser for incoming commands.
void parse(String s){
  JsonDocument receive;
  deserializeJson(receive, s);
  if("GD"==receive["cmd"]){sendDescription(receive);}
  if("RDY"==receive["cmd"]){setReadyState();}
  if("W"==receive["cmd"]){setWaitState();}
  if("GIS"==receive["cmd"]){sendInsertState(receive);}
  if("GG"==receive["cmd"]){sendGame(receive);}
}
void sendInsertState(){
        JsonDocument doc;
        doc["cmd"]="ISC";
        doc["insertState"]=insertState;
        doc["gameID"]=gameID;
        serializeJson(doc, Serial);
        Serial.print('\n');
}
void sendWaitState(){
        JsonDocument doc;
        doc["cmd"]="W";
        setWaitState();
        serializeJson(doc, Serial);
        Serial.print('\n');
}
void sendInsertState(JsonDocument receive){
        JsonDocument doc;   
        doc["cmd"]="ISC";
        doc["id"]=receive["id"];
        doc["insertState"]=insertState;
        doc["gameID"]=gameID;
        serializeJson(doc, Serial);
        Serial.print('\n');
}
void sendDescription(JsonDocument receive){
        JsonDocument doc;
        doc["cmd"]="GD";
        doc["id"]=receive["id"];
        doc["desc"]=description;
        serializeJson(doc, Serial);
        Serial.print('\n');
}
void sendGame(JsonDocument receive){
        JsonDocument doc;
        doc["cmd"]="GG";
        doc["id"]=receive["id"];
        doc["gameID"]=gameID;
        serializeJson(doc, Serial);
        Serial.print('\n');
}
void setReadyState(){
    state = 1;
}
void setWaitState(){
    state = 0;
}
void loop(void) {
  //Read incoming requests
  if (Serial.available() > 0) {
      parse(Serial.readString());
  }
  
  //Is a floppy in the drive?
  int insertVal = digitalRead(insertPin);
  if(insertVal != insertState && state == 1){
    insertState = insertVal;
    delay(1000);
    if(insertState==digitalRead(insertPin)){
      sendWaitState();
      //Get gamecard voltage/gameID
      float reading= analogRead(analogPin);
      gameID = reading;
      sendInsertState();
    }
  }
}

