# Importing Libraries 
import serial 
import time 
import serial.tools.list_ports
import json
import tkinter as tk

arduino = None;

class state:
	DEFAULT = 0;
	CONNECTING = 1;
	NOGAME = 2;

appState = state.NOGAME;

class logLevel:
    INFO = "\033[92mINFO: \033[0m";
    WARNING = "\033[93mWarning: \033[0m";
    ERROR = "\033[91mError: \033[0m";

def startGame(gameID):
	print("Todo: Start Game by ID.");
def getDescription(response):
	global appState;
	print("");
	print("{}{}{}".format(logLevel.INFO,"Connected to ",response["desc"]));
	appState = state.NOGAME;
	send("RDY");
def getGame(response):
	global appState;
	if(response["insertState"]==1):
		appState = state.DEFAULT;
		startGame(response["gameID"]);

def send(cmd, args=()):
	global arduino
	x = {
		"cmd": cmd,
		"args":args
	}
	try:
		print("{}Sending {}".format(logLevel.INFO,x));
		arduino.write(bytes(json.dumps(x), 'utf-8'));
			
	except:
		print("{}{}".format(logLevel.INFO,"Error"));
		if(cmd!="GD"):#avoid loop issues
			arduino = None;
			requestConnection();
	return id
def listener():
	global appState
	global arduino
	raw = None;
	try:
		raw = arduino.readline().decode("utf-8")
		if(len(raw)>0):
			response = json.loads(raw);
			print("\n{}Receiving {}".format(logLevel.INFO,response));
			if(response["cmd"]=="GD"):
				getDescription(response);
			if(response["cmd"]=="ISC"):
				getGame(response);
	except:
		if(appState!=state.CONNECTING):
			print("{}{}".format(logLevel.ERROR,"Lost Connection."));
			arduino = None;
			requestConnection();
			
def requestConnection():
	global appState;
	global arduino;
	if(arduino==None):
		if(appState!=state.CONNECTING):
			print("Connecting...", end='');
		else:
			print(".", end='');
			time.sleep(1);
		appState = state.CONNECTING;
		ports = serial.tools.list_ports.comports();
		for port, desc, hwid in sorted(ports):
			try: 
				arduino = serial.Serial(port=port, baudrate=115200, timeout=.1);
				send("GD");
			except:
				continue
def task():
    #Create a drive listener
	while(True):
		listener();
		if(appState==state.CONNECTING):
			requestConnection();
	
requestConnection();
window = tk.Tk();
window.title("Retro Madness Console");
window.attributes("-fullscreen", True);
label = tk.Label(window, text="Loading.")
label.pack();
window.after(200, task);
window.mainloop();



