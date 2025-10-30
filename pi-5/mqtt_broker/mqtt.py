import paho.mqtt.client as mqtt
import time
from mqtt_broker.broker import broker_ip

connection = False

def on_connect(client, userdata, flags, rc): 
    global connection
    if rc == 0:
        connection = True
        print(" Connection Successfull")
        client.subscribe("test")  
    else:
        print("Connection failed")

def on_message(client, userdata, msg) :
    print(f"recieved msg: [{msg.topic}] {msg.payload.decode()}")
    
    # Setup the client end 
    # on_connect and Client are all part of the MQTT libraries

client = mqtt.Client("PythonClient")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_ip, 1883)

# if the connection is not successfull wait
while not connection:
    client.loop()
    time.sleep(0.1)

client.loop_forever()



