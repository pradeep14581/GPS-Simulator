from tkinter import *
import tkinter.messagebox
import paho.mqtt.client as mqtt
import json
import threading
import time

LOGIN_PACKET_SEND_FLAG = False
LOGIN_PACKET_SEND_TIME = 0
LOGIN_SUCCESS = False
HEARTBEAT_PACKET_SEND_FLAG = False
HEARTBEAT_PACKET_SEND_TIME = 0
LOCATION_PACKET_SEND_FLAG = False
LOCATION_PACKET_SEND_TIME = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("DEVICE_SIMULATOR")
    client.connected_flag=True
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    if(msg.topic == "DEVICE_SIMULATOR"):
        print(" Received")
        payload = msg.payload;
        payload_dec = json.loads(payload)
        data = payload_dec['data']
        if(data[0] == 0x78 and data[1] == 0x78):  # command 0x78 0x78 
            if(data[3] == 0x01):  # login packet protocol no 0x01
                LOGIN_SUCCESS = True
                print(" Login Response Received")
                LOGIN_PACKET_SEND_FLAG = False
                LOGIN_PACKET_SEND_TIME = 0
                print("Login Success")
                print(LOGIN_SUCCESS)
                heartBeat()
                location()
            elif(data[3] == 0x23):  # Heartbeat packet protocol no 0x23
                print(" Heartbeat Response Received")
                HEARTBEAT_PACKET_SEND_FLAG = False
                HEARTBEAT_PACKET_SEND_TIME = 0
            elif(data[3] == 0x22):  #Location packet protocol no 0x22
                print(" Location Packet Response Received")
                LOCATION_PACKET_SEND_FLAG = False
                LOCATION_PACKET_SEND_TIME = 0               
    
def stopCallBack():
   #tkinter.messagebox.showinfo( "GPS Simulator", "Started")
    if tkinter.messagebox.askokcancel("Quit", "Do you really wish to stop GPS simulator?"):
        client.disconnect()
        client.loop_stop()
        widget1.destroy()
        r.destroy()

#def startCallBack():
#   tkinter.messagebox.showinfo( "GPS Simulator", "Started")
def buttonpress(event):
    """    print("Single Click, Button-l")     
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("broker.hivemq.com", 1883, 60)
    #client.loop_start()
    client.loop_forever()"""
    print("  jk")
def location():
    LOCATION_PACKET_SEND_FLAG = True
    LOCATION_PACKET_SEND_TIME = time.time()
    location_packet = [0x78, 0x78, 0x22, 0x22, 0x0F, 0x0C, 0x1D, 0x02, 0x33, 0x05, 0xC9, 0x02,0x7A, 0xC8,
                       0x18, 0x0C, 0x46, 0x58, 0x60, 0x00, 0x14, 0x00, 0x01, 0xCC, 0x00,
                       0x28, 0x7D, 0x00, 0x1F, 0x71, 0x00, 0x00, 0x01, 0x00, 0x08, 0x20, 0x86, 0x0D, 0x0A]
    location_json = {'data': location_packet}#,
    location_json = json.dumps(location_json)
    print(location_json)
    client.publish("DEVICE_ADAPTER", location_json)
    threading.Timer(5, location).start()

def heartBeat():
    heartBeatPacket = [0x78, 0x78, 0x0B, 0x23, 0xC0, 0x01, 0x22, 0x04, 0x00, 0x01, 0x00, 0x08, 
                       0x18, 0x72, 0x0D, 0x0A]
    heartBeat_json = {'data': heartBeatPacket}#,
    heartBeat_json = json.dumps(heartBeat_json)
    print(heartBeat_json)
    client.publish("DEVICE_ADAPTER", heartBeat_json)
    LOGIN_PACKET_SEND_TIME = time.time()
    LOGIN_PACKET_SEND_FLAG = True
    threading.Timer(30, heartBeat).start()
def Login():  
    print("Login")
    loginPacket = [0x78, 0x78, 0x11, 0x01, 0x03, 0x51, 0x60, 0x80, 0x80, 0x77, 0x92, 0x88, 0x22, 0x03,
                   0x32, 0x01, 0x01, 0xAA, 0x53, 0x36, 0x0D, 0x0A]
    login_json = {'data': loginPacket}#,
    login_json = json.dumps(login_json)
    print(login_json)
    client.publish("DEVICE_ADAPTER", login_json)
    LOGIN_PACKET_SEND_TIME = time.time()
    LOGIN_PACKET_SEND_FLAG = True
    
r = tkinter.Tk()
r.title('DEVICE SIMULATOR')
#widget = Button(r, text='Start Simulator', width=20, height=5, command = startCallBack)
#widget.pack(side=tkinter.LEFT)
widget1 = Button(r, text='Stop Simulator', width=20, height=5, command = stopCallBack)
widget1.pack(side=tkinter.RIGHT)
widget2 = Button(r, text='Login Packet', width=20, height=5, command = Login)
widget2.pack(side=tkinter.LEFT)
#widget3 = Button(r, text='Location Packet', width=10, height=5, command = Login)
#widget3.pack(side=tkinter.BOTTOM)
#widget.bind('<Button-1>', buttonpress)
client = mqtt.Client()
client.connected_flag=False
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()
#client.loop_forever()
LOGIN_SUCCESS = False
while not client.connected_flag: #wait in loop
     time.sleep(1)
pingTime = 0
while(1):
    
    if(LOGIN_PACKET_SEND_FLAG and (time.time() - LOGIN_PACKET_SEND_TIME)>=5):
        print("LOGIN Packet response not received Snd login packet again")
        LOGIN_PACKET_SEND_FLAG = False
        Login()
 #   if(LOGIN_SUCCESS and (time.time() - pingTime)>=5):
  #      pingTime = time.time()
  #      heartBeat()
    widget1.update_idletasks()
    widget1.update()
    #print(LOGIN_SUCCESS)
    
    #widget1.mainloop()
client.disconnect()
client.loop_stop()
