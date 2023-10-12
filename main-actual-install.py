# Program by Shore to measure two temperatures HWS and HWR, plus boiler status
# on a Raspberry Pi Pico W, and write the data to the IoT cloud ThingSpeak
# and display it there.  Thanks to hippy from Raspberry Pi Forum for program help.
#     Mathworks info
#     https://thingspeak.com/channels/2016936/
#        PicoW at Boiler
#        Channel ID: 2278931
#        Author: ShoreNice
#        Access: Public
#!/usr/bin/python
import machine
import urequests 
from machine import Pin,Timer
import network, time
import utime
import math
import random # esp8266 can ONLY get rand bits!!!!
####



#######


HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = 'KDYE4XJQZAPCCOXR'
ssid = 'bluebird27'
password = 'pggsk33!?'


# Configure Pico W as Station
sta_if=network.WLAN(network.STA_IF)
sta_if.active(True)
 
for _ in range(10):
        print('connecting to network...') 
        sta_if.connect(ssid, password)
        time.sleep(1)
        if sta_if.isconnected():
            print('Connected.')
            break
        time.sleep(11)
 
print('network config:', sta_if.ifconfig()) 


while True:
    print("Getting data to send")
   
  
   
    time.sleep(5)
    boilerstatus = (random.getrandbits(1)) 
    t1 = (random.getrandbits(7))
    t2 = (random.getrandbits(7))
    t3 = (random.getrandbits(7))
    t4 = (random.getrandbits(7))
    t5 = (random.getrandbits(7))
    t6 = (random.getrandbits(7))
    t7 = (random.getrandbits(7))
    #####
  
 
    readings = {'field1':t1, 'field2':t2, 'field3':t3,'field4':t4, 'field5':t5, 'field6':t6, 'field7' :t7, 'field8':boilerstatus}

    for retries in range(60):     # 60 second reboot timeout
        if sta_if.isconnected():
            print("Connected, sending")
            try:
                request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json = readings, headers = HTTP_HEADERS )  
                request.close()
                time.sleep(20)
                print("Write Data to ThingSpeak ",readings)
                print(" Successful  ")
                break
            except:
                print("Send failed")
                time.sleep(1) 
        else:
                print(" waiting for wifi to come back.....")
                time.sleep(1)
    else:
        print("Rebooting")
        time.sleep(1)
        machine.reset()   
print("Sent, waiting awhile")
time.sleep(10) 