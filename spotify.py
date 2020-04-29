import os
import sys
import json
import spotipy
import spotipy.util as util
import paho.mqtt.client as mqtt
import requests
from spotipy.oauth2 import SpotifyClientCredentials

username='David2339'
BROKER_ADDRESS='192.168.1.122'
def on_message(client, userdata,message):
    print(message.payload.decode('ascii'))
    if message.payload.decode('ascii') == 'spotifyOff':
        sp.pause_playback()
    else:
        songName = message.payload.decode('ascii')
        print(songName)
        result = sp.search(songName)
        print("result: ")
        songUri=result['tracks']['items'][0]['uri']
        print(songUri)
        sp.add_to_queue(songUri)
        print("Successfully added: " + songName + " to queue")
        sp.next_track()
        sp.start_playback()

scope = 'user-modify-playback-state'
token=util.prompt_for_user_token(username='David2339', scope=scope)
#token='BQCO7EZ3SLDMmF_YDQyWIew7r4PTg3bO7P72nd_xwfgOqhy0M8f2I'
sp = spotipy.Spotify(auth=token)

print(token)
client = mqtt.Client()
client.connect(BROKER_ADDRESS)
client.on_message=on_message
client.subscribe("/spotify")
client.loop_start()
try:
    while True:
        pass
except KeyboardInterrupt:
    pass
client.loop_stop()