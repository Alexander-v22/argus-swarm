import paho.mqtt.client as mqtt
import time
import broker

connection = False


def on_connect(client, userdata, flags, rc): 
    global connection
    if rc == 0:
        connnection = True
        print(" Connection Successfull")
    else:
        print("Connection failed")

def on_message(client, userdata, msg) :
    print("recieved msg: [{msg.topic}] {msg.payload.decode()}")
    
    # Setup the client end 
    # on_connect and Client are all part of the MQTT libraries



client = mqtt.Client("PythonClient ")
client.on_connect = on_connect

client.connect(broker)
# if the connection is not successfull wait
while not connection:
    time.sleep(0.1)

