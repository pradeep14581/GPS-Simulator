#!/usr/bin/env python
# coding: utf-8

# In[1]:



import paho.mqtt.client as mqtt
import json
import struct


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("DEVICE_ADAPTER")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    if(msg.topic == "DEVICE_ADAPTER"):
        print(" Received")
        payload = msg.payload;
        payload_dec = json.loads(payload)
        data = payload_dec['data']
        print(payload_dec)
        print(type(data))
        if(data[0] == 0x78 and data[1] == 0x78):  # login command 0x78 0x78
            if(data[3] == 0x01): #protocol no 0x01
                print(" Login Packet Received")
                login_response = [0x78, 0x78, 0x05, 0x01, 0x0, 0x05, 0x9F, 0xF8, 0x0D, 0x0A]
                login_json = {'data': login_response}#,
                login_json = json.dumps(login_json)
                print(login_json)
                client.publish("DEVICE_SIMULATOR", login_json)
            elif(data[3] == 0x23):  # Heartbeat packet protocol no 0x23
                #78 78 05 23 01 00 67 0E 0D 0A
                print(" HeartBeat Packet Received")
                heartbeat_response = [0x78, 0x78, 0x05, 0x23, 0x01, 0x00, 0x67, 0x0E, 0x0D, 0x0A]
                heartbeat_json = {'data': heartbeat_response}#,
                heartbeat_json = json.dumps(heartbeat_json)
                print(heartbeat_json)
                client.publish("DEVICE_SIMULATOR", heartbeat_json)                  
            elif(data[3] == 0x22):  # Location packet protocol no 0x22
                #78 78 05 23 01 00 67 0E 0D 0A
                dateTime = str(2000+data[4])+"-"+str(data[5])+"-"+str(data[6])+","+str(data[7])+":"+str(data[8])+":"+str(data[9])
                noOfGPSSatellites = data[10]
                aa= bytearray([data[11],data[12],data[13],data[14]]) 
                lat = int.from_bytes(aa, byteorder='big')/1800000
                aa1= bytearray([data[15],data[16],data[17],data[18]]) 
                long = int.from_bytes(aa, byteorder='big')/1800000      
                speed = data[19]
                
                print(" Location Packet Received")
                print(dateTime)
                
                location_response = [0x78, 0x78, 0x05, 0x22]#, 0x01, 0x00, 0x67, 0x0E, 0x0D, 0x0A]
                location_json = {'data': location_response}#,
                location_json = json.dumps(location_json)
                print(location_json)
                client.publish("DEVICE_SIMULATOR", location_json)
                
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()


# In[ ]:




