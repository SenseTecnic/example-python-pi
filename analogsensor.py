#!/usr/bin/python

# A python script that will get data from GPIO and send as a JSON event to WoTKit
import time
import httplib, urllib, urllib2, base64
import RPi.GPIO as GPIO

try:
    import json
except ImportError:
    import simplejson as json

GPIO.setmode(GPIO.BCM)
LIGHT_SENSOR_PIN = 4

#TODO: ADD YOUR SENSOR NAME AND CREDENTIALS
SENSOR_NAME = ''
USERNAME = ''
PASSWORD = ''
HOST = "wotkit.sensetecnic.com"
URL = "/api/v1/sensors/%s/data" % SENSOR_NAME


# Utility function to measure analogue sensors via digital pins
# it charges a capacitor and measures the time it takes to uncharge
# giving an idea of the value in the analogue sensor.
def RCtime (PiPin):

    return 10000; #TODO: REMOVE 

    measurement = 0
    # Discharge capacitor
    GPIO.setup(PiPin, GPIO.OUT)
    GPIO.output(PiPin, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(PiPin, GPIO.IN)
    # Count loops until voltage across
    # capacitor reads high on GPIO
    while (GPIO.input(PiPin) == GPIO.LOW):
      measurement += 1
    return measurement

def getLight(sensor_data):
    chargeTime = RCtime(LIGHT_SENSOR_PIN)
    # transorming time in capacitor charge to light values
    light = (  chargeTime * -1 ) + 200000
    sensor_data['light'] = light
    sensor_data['value'] = light

def main():

    sensor_data = {
        "light":"0"
    }

    auth = base64.encodestring('%s:%s' % (USERNAME, PASSWORD)).replace('\n', '')
    headers = {"Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain",
            "Authorization": "Basic %s" % auth
    }  

    while True:

        getLight(sensor_data)
        params = urllib.urlencode(sensor_data)
        conn = httplib.HTTPConnection(HOST);
        conn.request("POST", URL, params, headers)
        response = conn.getresponse()
        print "Response Code: %s" % response.status
        conn.close()
        
        time.sleep(5)

    
if __name__ == "__main__":
    main()
    


