#include <ArduinoJson.h>

//Define used pins
int gameSensor = A0; 
int cartridgeSensor = 3;
int resetButton = 4;
int LED = 5;

//Define global variables
String description= "Retro Madness Cartridge Reader v0.2";
int state = 0;
JsonDocument buttonState;

void setup(void) {
  buttonState["insert"]=-1;
  buttonState["reset"]=-1;
  pinMode(gameSensor, INPUT);//floppy resistance to determin game id.
  pinMode(cartridgeSensor, INPUT);//Is floppy in drive?
  pinMode(resetButton, INPUT);//is reset button pressed?
  pinMode(LED, OUTPUT); //LED
  digitalWrite(LED, HIGH); //LED always on
  Serial.begin(115200);
};

//command parser for incoming commands.
void parse(String s){
  JsonDocument receive;
  deserializeJson(receive, s);
  if("GD"==receive["cmd"]){sendDescription();}
  if("RDY"==receive["cmd"]){setReadyState();}
}

void sendInsertState(int state,int gameID){
        JsonDocument doc;
        doc["cmd"]="ISC";
        doc["insertState"]=state;
        doc["gameID"]=gameID;
        serializeJson(doc, Serial);
        Serial.print('\n');
}

void sendDescription(){
        buttonState["insert"]=-1;
        buttonState["reset"]=-1;
        state=0;
        JsonDocument doc;
        doc["cmd"]="GD";
        doc["desc"]=description;
        serializeJson(doc, Serial);
        Serial.print('\n');
}

void sendReset(int gameID){
        //Blink LED on reset
        digitalWrite(LED, LOW);
        JsonDocument doc;
        doc["cmd"]="RST";
        doc["gameID"]=gameID;
        serializeJson(doc, Serial);
        Serial.print('\n');
        delay(1000);            
        digitalWrite(LED, HIGH);
}
void setReadyState(){
    state = 1;
}

boolean singlePress(String event,int value){
  if(buttonState[event]!=value){
    buttonState[event]=value;
    return true;
  }
  return false;
}

void loop(void) {

  //Read incoming requests
  if (Serial.available() > 0) {
      parse(Serial.readString());
  }
  
  //We only want to send updates after the program is ready to receive data.
  if(state==1){
    
    //Send state of floppy within the drive only when it has changed (Inserted/Removed).
    int insertVal = digitalRead(cartridgeSensor);
    int gameID = analogRead(gameSensor);
    if(insertVal==0){gameID=-1;};
    if(singlePress("insert",insertVal)){
        sendInsertState(insertVal,gameID);
    }

    //Send state of reset only when it has changed from unpressed to pressed.
    int reset = digitalRead(resetButton);
    if(singlePress("reset",reset)&& reset==1){
        sendReset(gameID);
    }
  }
}