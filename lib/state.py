"""
    SingularityHA
    ~~~~~~~~~~~~~~~~~~~~~

    State storage into MySQL

    :copyright: (c) 2013 - by Internet by Design Ltd
    :license: GPL v3, see LICENSE for more details.

"""
from peewee import *
import datetime
import time
from config import config
import logging
import json
import os
import mosquitto

os.environ['TZ'] = 'Pacific/Auckland'

# Pulls configuration from the config module
server = config.get("database", "host")
username = config.get("database", "username")
password = config.get("database", "password")
database = config.get("database", "database")
broker = str(config.get("mqtt", "host"))
port = int(config.get("mqtt", "port"))
our_db = MySQLDatabase(database, host=server, user=username, passwd=password)

# Start up logging
logger = logging.getLogger(__name__)
logger.info("State library started...")

# This is the definition of the database model
class StateModel(Model):
    class Meta:
        database = our_db

class StateTable(StateModel):
    device = CharField(max_length=255)
    state = CharField(max_length=255)
    attributes = TextField(null=True)
    lock = BooleanField(default=0)
    lastChange = DateTimeField(default=datetime.datetime.now())

our_db.connect()

def on_connect(mosq, obj, rc):
    if rc == 0:
        #rc 0 successful connect
        logger.debug("State connected to MQTT")
    else:
        raise Exception

def on_publish(mosq, obj, val):
    logger.debug("published")

def cleanup():
    ser.close()
    mqttc.disconnect()


def on_disconnect(mosq, obj, rc):
    print("Disconnected successfully.")

mypid = os.getpid()
client_uniq = "singuarltiyHA_state"+str(mypid)
mqttc = mosquitto.Mosquitto(client_uniq)

mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_disconnect = on_disconnect
mqttc.connect(broker, port, 60, True)


def set(module, device, state, attributes=None):
	""" Set the state of the specified device"""
	try:
		acquire_lock(device)
	except:
		#state object doesn't exist yet
		pass
	try:
		state_object = StateTable.select().where(StateTable.device == device).get()
	except:
		state_object = StateTable()

	state_object.device = device
	state_object.state = state
	state_object.attributes = attributes
	state_object.lastChange = datetime.datetime.now()
	state_object.save()
	logger.debug("Setting state for" + str(device) + "with state" + str(state) + "and attributes" + str(attributes))
	release_lock(device)
	logger.debug("SETTING MQTT STATE")
	attributes_mqtt = {"device" : device, "module" : module, "state" : state, "attributes" : json.loads(attributes)}
	logger.debug("MQTT:", attributes_mqtt)
	mqttc.publish("state", json.dumps(attributes_mqtt))

	
def get(device):
    """ Simple function to pull the state of a device from the DB """
    try:
        state = StateTable.select().where(StateTable.device == device).get()
        state.attributes = json.loads(state.attributes)
    except:
        state = {}
    return state


def acquire_lock(device):
    """ Get lock over the state of a device to prevent clashes """
    loggger.debug("attempting to get lock for device" + device)
    while True:
        if not StateTable.select().where(StateTable.device == device).get().lock:
            state_obj = StateTable.select().where(StateTable.device == device).get()
            state_obj.lock = True
            state_obj.save()
            loggger.debug("got lock for device" + device)
            break
        time.sleep(1)


def release_lock(device):
    """ Unlock once we have finished editing the state """
    state_obj = StateTable.select().where(StateTable.device == device).get()
    state_obj.lock = False
    state_obj.save()


