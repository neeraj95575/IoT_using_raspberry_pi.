import sys
import urllib.request
from time import sleep
import Adafruit_DHT as dht
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_TRIGGER = 18
GPIO_ECHO = 15
GPIO_IR = 14

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_IR, GPIO.IN)


# Enter Your API key here
myAPI = 'MMC01Y20ABML1ZN7' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI


def DHT22_data():
	# Reading from DHT22 and storing the temperature and humidity
	humi, temp = dht.read_retry(dht.DHT22, 2) 
	return humi, temp
    

def ultrasonic_sensor():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    dist = (TimeElapsed * 34300) / 2
    return dist
while True:
		humi, temp = DHT22_data()
		dist = ultrasonic_sensor()		
		state=GPIO.input(GPIO_IR)
		# If Reading is valid
		if isinstance(humi, float) and isinstance(temp, float) and isinstance(dist, float)and isinstance(state, int):
			# Formatting to two decimal places
			humi = '%.2f' % humi 					   
			temp = '%.2f' % temp
			dist =  '%.2f' % dist
			print("humidity = ",humi)
			print("temperature = ",temp)
			print("distance = ",dist)
			print("state = ",state)
			# Sending the data to thingspeak
			conn = urllib.request.urlopen(baseURL + '&field1=%s&field2=%s&field3=%s&field4=%s' % (temp, humi,dist,state))
			print (conn.read())
			# Closing the connection
			conn.close()
		else:
			print( 'Error')
		# DHT22 requires 2 seconds to give a reading, so make sure to add delay of above 2 seconds.
		sleep(20)
                      

