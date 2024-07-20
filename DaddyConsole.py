# Importing Libraries 
from os import close
import serial 
import time 
import serial.tools.list_ports
import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
arduino = None;
id = 0; 
timeout = 1;
verbose = True;
state = 0;
def requestDescription():
	send("GD");
def setDescription():
	print("{}INFO: {}Connected to {} on {}: {} [{}]".format(bcolors.OKGREEN,bcolors.ENDC,response["desc"],port, desc, hwid));
	send("RDY");
	state = 1;
def error():
	print("{}ERROR: {}Unable to connect to device".format(bcolors.FAIL,bcolors.ENDC))
	time.sleep(timeout*5)
	connect();	
def connect():
	print("Finding Device...");
	ports = serial.tools.list_ports.comports()
	for port, desc, hwid in sorted(ports):
		try: 
			global arduino
			arduino = serial.Serial(port=port, baudrate=115200, timeout=.1)
			requestDescription()
			response = receive()
			if("GD"==response["cmd"]):
				print("{}INFO: {}Connected to {} on {}: {} [{}]".format(bcolors.OKGREEN,bcolors.ENDC,response["desc"],port, desc, hwid))
				state = 1;
				break
			arduino = None
			continue
		except: 
			arduino = None
			continue
def parse(cmd):
	print(cmd)
def send(cmd, args=()):
	global id 
	id += 1
	if(id>=1000):
		id = 1;
	x = {
		"cmd": cmd,
		"id": id,
		"args":args
	}
	try:
		arduino.write(bytes(json.dumps(x), 'utf-8')) 
	except:
		error()
	time.sleep(timeout)
	return id
def receive():
			try:
				raw = arduino.readline().decode("utf-8")
				try:
					if(len(raw)>0):
						response = json.loads(raw)
						if(verbose):
							print("{}VERBOSE: {}{}".format(bcolors.OKBLUE,bcolors.ENDC,response))
						parse(response)
						return response
				except: 
					print("{}ERROR: {}Unknown response ""{}""".format(bcolors.FAIL,bcolors.ENDC,raw))
				
			except:
				error()
			
				
connect()
#Handle if no device available
if(arduino==None):
	error()
while 1==1: #create a listener
	receive()
	