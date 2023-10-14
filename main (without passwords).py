# Program by Shore  Access: Public
#     https://thingspeak.com/channels/2278931/
#        PicoW at Boiler  Channel ID: 2278931  Author: ShoreNice
#       
#!/usr/bin/python
import machine
import urequests 
from machine import Pin,Timer
import network, time
import utime
import math
import random # esp8266 can ONLY get rand bits!!!!
# rand bit 1 is 0 or 1, rand bit 2 is 0 to 3, rand bit 3 is 0 to 7, rand bit 4 is 0 to 15
# rand bit 5 is 0 to 31, rand bit 6 is 0 to 63, rand bit 7 is 0 to 127
####

HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = 'KDYEsecretPCCOXR'
ssid = 'bluesecret'
password = 'pggssecret'

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
   
    t1a = (random.getrandbits(7))
    t1 = (100 * (t1a/127))
    t2a = (random.getrandbits(7))
    t2 = (4000 * (t2a/127))
    t3 = (random.getrandbits(7))
    t4a = (random.getrandbits(7))
    t4 = (30 * (t4a/127))
    t5a = (random.getrandbits(7))
    t5 = (45 * (t5a/127))
    t6a = (random.getrandbits(7))
    t6 = (200000 * (t6a/127))
    t7a = (random.getrandbits(7))
    t7 = (50000 * (t7a/127))
    # t8 will be boilerstatus toggled 0 or 1
    boilerstatus = (random.getrandbits(1)) 
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
