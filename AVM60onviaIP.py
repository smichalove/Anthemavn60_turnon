#!/usr/bin/env python3
# you need to install: python-anthemav
# https://github.com/nugget/python-anthemav/
# Pulse conversion from constant 12V input
#This assumes your Mark Levinson APM is on Standby as start state
#Your input to the Mark Levinson Should connect to GPIO21 for + and a GRND
#The control Signal from constant high or low should connect to a 12 V relay
#the switch signals from the relay to toggle on/off should be connected to GPIO26 and GRND
# Radpberry Pico connected to USB on TV
# Pico siglnalling pin connected on GPIO20 pico (GP16) of Pi
'''
https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython
Conntect USB-C of pico to USB on TV
Using Circuit Python on Rasbarry Pico code.py =
GP16 on pico connected to GPIO21 on pi

'''
import signal                   
import sys
from time import sleep 
import time
import RPi.GPIO as GPIO
from gpiozero import LED, Button
from gpiozero.tools import booleanized, all_values
import datetime
#load for Anthem:https://github.com/nugget/python-anthemav/blob/master/example.py
import argparse
import asyncio
import anthemav # install:https://github.com/nugget/python-anthemav/
import logging
log = logging.getLogger(__name__)
#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BCM)
AMP=21 #Control Signal to amp
GPIO.setup(AMP, GPIO.OUT)
pico = 20
GPIO.setup(pico, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
Button.was_held = False


## Anthem Fuctions
async def test():
    parser = argparse.ArgumentParser(description=test.__doc__)
    parser.add_argument("--host", default="192.168.50.60", help="IP or FQDN of AVR") ## Set Anthem IP
    parser.add_argument("--port", default="14999", help="Port of AVR")
    parser.add_argument("--verbose", "-v", action="count")

    args = parser.parse_args()


    level = logging.ERROR

    logging.basicConfig(level=level)

    def log_callback(message):
        log.info("Callback invoked: %s" % message)
    
    if GPIO.input(pico) == 1:

        host = args.host
        port = int(args.port)

        log.info("Connecting to Anthem AVR at %s:%i" % (host, port))

        conn = await anthemav.Connection.create(
            host=host, port=port, loop=loop, update_callback=log_callback
        )

        log.info("Power state is " + str(conn.protocol.power))
        conn.protocol.power = True
        log.info("Power state is " + str(conn.protocol.power))

        #await asyncio.sleep(2, loop=loop)
        log.info("Anthem power On" + str(conn.protocol.power))

        conn.protocol.power = True ## Turn Power On
        log.info("Anthem power On" + str(conn.protocol.power))
        sleep(1)
        conn._closing = True # Close Connection
        conn.halt
        conn.auto_reconnect = False
        log.info("Auto Reconnect " + str(conn.auto_reconnect))
        log.info("Connection halt " + str(conn.halt))
    
        
      ## end Anthem functions

def held(btn): #when siglnal is high and stays high
    btn.was_held = True
    datetime_object = datetime.datetime.now()
    print(datetime_object)
    print("button was held ")
    GPIO.output(AMP, 1) 
    sleep(.3) 
    GPIO.output(AMP, 0)

def released(btn): #when signal is low and stays low
    if not btn.was_held:
        datetime_object = datetime.datetime.now()
        print(datetime_object)
        print("Release1")
        #GPIO.output(AMP, 1) 
        sleep(.3) 
        GPIO.output(AMP, 0)        
        pressed()
    else:       
        print(time.time())
        datetime_object = datetime.datetime.now()
        print(datetime_object)
        print("Release2")
        GPIO.output(AMP, 1) 
        sleep(.3) 
        GPIO.output(AMP, 0) 
   
    btn.was_held = False

def pressed():
    datetime_object = datetime.datetime.now()
    print(datetime_object)
    print("button was pressed not held")

btn = Button(26,bounce_time = .001) # relay is on pin GPIO26  and GRND

if __name__ == '__main__':
    runonce = True
    try:
        print ("listning...")              
        while True: 
            btn.when_held = held
            btn.when_released = released
            sleep(1)
            if GPIO.input(pico) == 1 and runonce: # if port 20 == 1, connect to Athhem AVM60 and turn it on when the Pico turns off with TV via USB
                state = GPIO.input(pico)
                print ("gpio state:",state)
                print("TV is On, Turning on everything else")
                datetime_object = datetime.datetime.now()
                print(datetime_object)
                print ("Connect to Anthem and turn on...")
                logging.basicConfig(level=logging.ERROR)
                loop = asyncio.get_event_loop()
                loop.run_until_complete(test())
                sleep(1)
                print ("Wait for Anthem")
                sleep(1)
                print(datetime_object)
                print ("Anthem On, listning for a button...")
                runonce = False
            else:
                if GPIO.input(pico) == 0:
                    state = GPIO.input(pico)
                    print ("gpio state:",state)
                    runonce = True
                    print ("TV Off, Listning")
                    #btn.when_held = held
                    btn.when_released = released
                    sleep(1)
                
    # run until a keyboard interupt
    except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C  
        print ("\n", runonce)# print value of counter  

    finally:
        GPIO.cleanup() 
         
