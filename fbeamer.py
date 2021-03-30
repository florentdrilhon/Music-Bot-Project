apiVersion = 'v9.0'

import requests, sys
import time


class FBeamer():
    def __init__(self, pageAccessToken, VerifyToken):
        self.pageAccessToken = pageAccessToken
        self.VerifyToken = VerifyToken


    #function to register the webhook
    def registerHook(self, request):
        #webhook verification
        verify_token = request.args.get("hub.verify_token")
        # Check if sent token is correct
        if verify_token == self.VerifyToken:
            # Responds with the challenge token from the request
            return request.args.get("hub.challenge")
        return 'Unable to authorise.'


    # function to receive a message and extract the main content
    def receiveMessage(self, request):
        self.log("\nReceiving message, handling content\n")
        data = request.get_json()
        # check if there is a response
        if data['entry'] and data['object'] == 'page':
          #extracting info
          message = data['entry'][0]['messaging'][0]['message']
          nlp=message['nlp']
          senderId = data['entry'][0]['messaging'][0]['sender']['id']
          intent=self.extractIntent(nlp)
          #self.log('Message intent :' + intent)
          obj = {'data': data, 'message': message,'nlp': nlp, 'senderId': senderId, 'intent': intent}
        # else sending back an empty response
        else : obj = None
        return obj


    # function to extract intent from a response from the webhook
    def extractIntent(self, nlp):
      if len(nlp["intents"])>0 and nlp["intents"][0]["confidence"]>=0.65 :
        return nlp["intents"][0]["name"]
      else:
        return None


    # function to extract an entity in the NLP object given the name of the Entity
    def extractEntity(self, nlp, entityName):
      if entityName in nlp["entities"] and nlp["entities"][entityName][0]["confidence"]>=0.60:
        return nlp["entities"][entityName][0]["value"]
      else :
        self.log("Could not find entity : " + entityName)
        return None

      

    # function to send a response to the API
    def sendMessage(self, obj):
        self.log("\nSending response\n")
        response = requests.post(
                'https://graph.facebook.com/v9.0/me/messages?access_token=' +
                self.pageAccessToken,
                json=obj).json()
        return response

    # function to format a text response and then send it
    def txtSender(self, sender_id,text, messaging_type='RESPONSE'):
      obj={
        'recipient':{
          'id': sender_id
        },
        'message':{
          "text": text
          }
      }
      return self.sendMessage(obj)

    def typing(self, sender_id, waiting_time):
      res1=self.sendMessage({'recipient': sender_id, 'sender_action' : 'typing_on'})
      time.sleep(waiting_time)
      res2=self.sendMessage({'recipient': sender_id, 'sender_action' : 'typing_off'})


    # function to format and send image responses
    def imgSender(self, sender_id, img_url, messaging_type='RESPONSE'):
      obj={
        'recipient':{
          'id': sender_id
        },
        'message':{
          "attachment": {
            "type": "image",
            "payload" : {
              "url": img_url
              }
            }
          }
        }
      return self.sendMessage(obj)

    def log(self, message):
        print(message)
        sys.stdout.flush()

    # TODO function to extract the content of a message
