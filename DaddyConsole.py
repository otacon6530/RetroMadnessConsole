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

print("Finding Device...")
ports = serial.tools.list_ports.comports()
arduino = None;
id = 0;
timeout = 2;
value = None;
verbose = True;
state = 0;

def send(cmd):
	global id 
	id += 1
	x = {
		"cmd": cmd,
		"id": id
	}
	arduino.write(bytes(json.dumps(x), 'utf-8')) 
	time.sleep(timeout)
	return id
def receive():
		raw = arduino.readline().decode("utf-8")
		if(len(raw)>0):
			try:
				response = json.loads(raw)
			except: 
				print("{}ERROR: {}Unknown response ""{}""".format(bcolors.FAIL,bcolors.ENDC,raw))
				quit()
			if(verbose):
				print("{}VERBOSE: {}{}".format(bcolors.OKBLUE,bcolors.ENDC,response))
			return response
#Handshake
for port, desc, hwid in sorted(ports):
	try: 
		arduino = serial.Serial(port=port, baudrate=9600, timeout=.1)
		i = send("GD")
		response = receive()
		if(i==response["id"]):
			print("{}INFO: {}Connected to {} on {}: {} [{}]".format(bcolors.OKGREEN,bcolors.ENDC,response["desc"],port, desc, hwid))
			send("RDY")
			state = 1;
			break
		arduino = None
		continue
	except: 
		arduino = None
		continue
#Handle if no device available
if(arduino==None):
	print("{}ERROR: {}Unable to connect to device".format(bcolors.FAIL,bcolors.ENDC))
	exit
while state==1: 
	receive()
	