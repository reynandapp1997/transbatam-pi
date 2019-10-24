import RPi.GPIO as GPIO
import time
import requests
import serial
import string
import pynmea2

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

state = False
led_red_pin = 18
led_green_pin = 23
button_pin = 17

GPIO.setup(led_red_pin, GPIO.OUT)
GPIO.setup(led_green_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def listenButtonPressed(state_pressed):
	global state
	if state_pressed == False:
		state = not state
		time.sleep(0.2)

def sendCoordinates(lat, long):
	domain = 'https://transbatam-api.herokuapp.com/'
	body = {
		'latitude': lat,
		'longitude': long,
		'busId': '5daeccabea6939001705f502'
	}
	response = requests.post(domain + 'api/location', data = body)
	print response.text
	time.sleep(30)

try:
	print 'START'
	while True:
		button_state = GPIO.input(button_pin)
		listenButtonPressed(button_state)
		if state == True:
			GPIO.output(led_green_pin, 1)
			GPIO.output(led_red_pin, 0)

			port="/dev/ttyAMA0"
			ser=serial.Serial(port, baudrate=9600, timeout=0.5)
			dataout = pynmea2.NMEAStreamReader()
			newdata=ser.readline()

			if newdata[0:6] == "$GPRMC":
				newmsg=pynmea2.parse(newdata)
				lat=newmsg.latitude
				lng=newmsg.longitude
				print lat
				print lng
				sendCoordinates(lat, lng)
		else:
			GPIO.output(led_red_pin, 1)
			GPIO.output(led_green_pin, 0)

except KeyboardInterrupt:
	print 'END'
	GPIO.cleanup()
