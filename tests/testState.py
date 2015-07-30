import os,sys,inspect
import json
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import time

from lib import state

def testState():
	#state.StateTable.create_table()
	attributes = {}
	attributes['brightness'] = 8
	state.set("LimitlessLED", "LoungeLight", "on", json.dumps(attributes))
	time.sleep(2)
	attributes['brightness'] = 0
	state.set("LimitlessLED", "LoungeLight", "off", json.dumps(attributes))
