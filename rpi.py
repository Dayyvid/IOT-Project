import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import datetime
import time
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# configuration
MOTION_SENSOR_PIN = 18

# URL for hue lightbulb api
hueURL = "http://192.168.1.113/api/ueHzP8967ViWMnm11PDCY3QdIhlhy-LrxY5wUKLn/lights/1/state"

lightbulbURL = "http://192.168.1.116:5000/lightbulb"

# variables for mqtt
BROKER_ADDRESS="192.168.1.122"

# spotify search url
spSearch = "https://api.spotify.com/v1/search"

#spotify add to queue url
spAdd = "https://api.spotify.com/v1/me/player/queue"
 
def on_message(client, userdata, message):
	# if message tells rpi to turn on security system
	if message.payload.decode('ascii') == "securitySystemOn": 
		print("Got on message")
		r = requests.get(lightbulbURL)
		data = r.json()
		print(data)
		client.publish("/spotify", data['songName'])
		xy = calculateXY(int(data['red']), int(data['green']), int(data['blue']))
		data = {"on":True, "sat":int(data['saturation']), "bri":int(data['brightness']), "hue":int(data['hue']), "xy":xy}
		r = requests.put(url=hueURL,data=json.dumps(data),timeout=5)
		print(r)
	elif message.payload.decode('ascii') == "securitySystemOff":
		print("Got off message")
		data = {"on": False}
		r = requests.put(url=hueURL, data=json.dumps(data), timeout=5)
		client.publish("/spotify", "spotifyOff")
def main():
	print("test.py script started")
	#set up breadboard
	GPIO.cleanup()
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(MOTION_SENSOR_PIN, GPIO.IN)
	
	# set up mqtt
	client = mqtt.Client()
	client.connect(BROKER_ADDRESS)
	client.on_message=on_message
	client.subscribe("/fromArduino")
	client.loop_start()
	try:
		while True:
			motion_output = GPIO.input(MOTION_SENSOR_PIN)
			print(motion_output)
			if motion_output == 1:
				client.publish("/fromRPi", "arduinoLedOn")
			time.sleep(0.50)	
	except KeyboardInterrupt:
		pass
	client.loop_stop()
	GPIO.cleanup()

def calculateXY(red, green, blue):
	if red > 0.04045:
		red = ((red+0.055)/(1.0+0.055)) ** 2.4
	else:
		red = red/12.92
	if green > 0.04045:
		green = ((green+0.055)/(1.0+0.055)) ** 2.4
	else:
		green = green/12.02
	if blue > 0.04045:
		blue = ((blue+0.055)/(1.0+0.055)) ** 2.4
	else:
		blue = blue/12.92
	x = red * 0.664511 + green*0.154324 + blue*0.162028
	y = red * 0.283881 + green*0.668433+blue*0.047675
	z = red * 0.000088 + green*0.072310 + blue*0.986039
	return[x/(x+y+z), y/(x+y+z)]

if __name__ == "__main__":
	main()
