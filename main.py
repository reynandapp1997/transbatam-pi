import RPi.GPIO as GPIO
import time
import requests
from requests.exceptions import HTTPError
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
		'busId': '5daeccb5ea6939001705f503'
	}
	try:
		response = requests.post(domain + 'api/location', data = body)
		response.raise_for_status()
	except HTTPError as http_err:
		print http_err
	except Exception as err:
		print err
	else:
		if response.status_code == 201:
			print "Berhasil mengirim koordinat"
		else:
			print "Tidak berhasil mengirim koordinat"
	time.sleep(5)

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
