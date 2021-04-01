from flask import Flask, request
from fbeamer import FBeamer
import random
from dotenv import load_dotenv
import os, sys
import time

from spotifyAPI import spotifyConnector
from conversationer import conversationer
env_path = './.env'
load_dotenv(dotenv_path=env_path)


# loading environement variables
pageAccessToken=os.getenv("PAGE_ACCESS_TOKEN")
verifyToken=os.getenv("VERIFY_TOKEN")

spotifyClientId=os.getenv("SPOTIFY_CLIENT_ID")
spotifySecretId=os.getenv("SPOTIFY_SECRET_ID")


app = Flask(__name__)
f=FBeamer(pageAccessToken, verifyToken)
spotiConnector=spotifyConnector(spotifyClientId, spotifySecretId)
conversationer = conversationer(spotiConnector, f)


# default endpoint
@app.route('/', methods=['GET'])
def home():
  return 'server running'

#test for spotify api
@app.route('/track', methods=['GET'])
def data():
  track=spotiConnector.searchTrack('Billie Jean')
  return track


#test for spotify api artist search
@app.route('/artist', methods=['GET'])
def artist():
  artist=spotiConnector.searchArtist('Michael Jackson')
  return artist



# register the webhook
@app.route('/webhook',methods=['GET'])
def verify():
  return f.registerHook(request)



@app.route("/webhook", methods=['POST'])
def function():
  message=  f.receiveMessage(request)
  if message:
    conversationer.main(message)
    return 'ok', 200
  else:
    f.log("Could not read message")
    return 'not ok', 500


if __name__ == "__main__":
  app.run( 
    # Starts the site  # EStablishes the host, required for repl to detect the site
		port=80,
    debug=True,
    threaded=True
	)