# Importing Libraries 
from os import close
import serial 
import time 
import serial.tools.list_ports
import json

arduino = None;

def log(msg,level):
	print("{}INFO: {}".format(bcolors.OKGREEN,bcolors.ENDC,response["desc"],port, desc, hwid)+msg);
def send(cmd, args=()):
	x = {
		"cmd": cmd,
		"args":args
	}
	try:
		arduino.write(bytes(json.dumps(x), 'utf-8'));
	except:
		log("Error","error");
	return id

print("Finding Device...");
ports = serial.tools.list_ports.comports();
for port,  desc, hwid in sorted(ports):
	try: 
		arduino = serial.Serial(port=port, baudrate=115200, timeout=.1)
		send("GD",port);
		continue
	except:
		continue

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