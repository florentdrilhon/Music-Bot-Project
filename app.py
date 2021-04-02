from flask import Flask, request
import random
from dotenv import load_dotenv
import os, sys
import time

from src.fbeamer import FBeamer
from src.spotifyAPI import spotifyConnector
from src.conversationer import conversationer


env_path = './.env'
load_dotenv(dotenv_path=env_path)


# loading environement variables
pageAccessToken=os.getenv("PAGE_ACCESS_TOKEN")
verifyToken=os.getenv("VERIFY_TOKEN")

spotifyClientId=os.getenv("SPOTIFY_CLIENT_ID")
spotifySecretId=os.getenv("SPOTIFY_SECRET_ID")

#initialization of the instances
app = Flask(__name__)
f=FBeamer(pageAccessToken, verifyToken)
spotiConnector=spotifyConnector(spotifyClientId, spotifySecretId)
conversationer = conversationer(spotiConnector, f)


# default endpoint
@app.route('/', methods=['GET'])
def home():
  return 'server running'


# register the webhook
@app.route('/webhook',methods=['GET'])
def verify():
  return f.registerHook(request)


# receive message from the webhook
@app.route("/webhook", methods=['POST'])
def function():
  message=  f.receiveMessage(request)
  if message:
    conversationer.main(message)
    return 'ok', 200
  else:
    f.log("Could not read message")
    return 'not ok', 500


# this part is a little different in the repl.it
if __name__ == "__main__":
  app.run( 
    # Starts the site  # EStablishes the host, required for repl to detect the site
		port=80,
    debug=True,
    threaded=True
	)