apiVersion = 'v2.6'

import requests, sys
import time
import json


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
        if data['entry'] and data['object'] == 'page' :
          #extracting info
          message = data['entry'][0]['messaging'][0]['message']
          nlp=message['nlp']
          senderId = data['entry'][0]['messaging'][0]['sender']['id']
          intent=self.extractIntent(nlp)
          #self.log('Message intent :' + intent)
          obj = {'data': data, 'message': message,'nlp': nlp, 'senderId': senderId, 'intent': intent}
          # notify the user that the message is received
          self.log("Message received correctly, mark as seen")
          self.markSeen(senderId)
        # else sending back an empty response
        else : obj = None
        return obj


    # function to extract intent from a response from the webhook
    def extractIntent(self, nlp):
      if len(nlp["intents"])>0 and nlp["intents"][0]["confidence"]>=0.65 :
        intent= nlp["intents"][0]["name"]
        self.log("Intent detected : {}".format(intent))
        return intent

      else:
        return None


    # function to extract an entity in the NLP object given the name of the Entity
    def extractEntity(self, nlp, entityName):
      if entityName in nlp["entities"] and nlp["entities"][entityName][0]["confidence"]>=0.60:
        entity= nlp["entities"][entityName][0]["value"]
        self.log("Entity {} found : {}".format(entityName, entity))
        return entity
      else :
        self.log("Could not find entity : " + entityName)
        return None

      

    # function to send a response to the API
    def sendMessage(self, obj):
        params={
          "access_token": self.pageAccessToken
        }
        headers={
          "Content-Type" : "application/json"
        }
        data=json.dumps(obj)
        response = requests.post(
                'https://graph.facebook.com/v2.6/me/messages',
                params=params,
                headers=headers,
                data=data
                )
        # if error report it
        if response.status_code != 200:
            self.log(response.status_code)
            self.log(response.text)

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

    def quickReplies(self,senderId, messageText, button1, button2):
      obj= { 
        'recipient':{
          'id': senderId
        },
        'message':{
              "text":messageText,
              "quick_replies":[
                {
                  "content_type": "text",
                  "title": button1,
                  "payload": "button1"
                },
                {
                  "content_type": "text",
                  "title": button2,
                  "payload": "button2"
                }
              ]
            }
        }
      return self.sendMessage(obj)

    # special template to send user friendly tracks
    def trackSender(self, senderId, tracks):
      elements=[
                      {
                      "title":track["name"],
                      "image_url":track["album"]["image"],
                      "subtitle":track["artist"]["name"],
                      "default_action": {
                        "type": "web_url",
                        "url": track["link"],
                        "webview_height_ratio": "COMPACT",
                    },
                  "buttons":[
                    {
                      "type":"web_url",
                      "url": track["link"],
                      "title":"Listen here"
                    }              
                   ]      
                }
              for track in tracks]
      obj={
          'recipient':{
            'id': senderId
          },
          'message':{
            "attachment":{
              "type": "template",
              "payload":{
                  "template_type":"generic",
                  "elements": elements
            }
          } 
        }
      }
      return self.sendMessage(obj)


    # special template to send user friendly artists
    def artistSender(self, senderId, artists):
      elements=[
                      {
                      "title":artist["name"],
                      "image_url":artist["image"],
                      "default_action": {
                        "type": "web_url",
                        "url": artist["link"],
                        "webview_height_ratio": "TALL",
                    },
                  "buttons":[
                    {
                      "type":"web_url",
                      "url": artist["link"],
                      "title":"Listen here"
                    }              
                   ]      
                }
              for artist in artists]
      obj={
          'recipient':{
            'id': senderId
          },
          'message':{
            "attachment":{
              "type": "template",
              "payload":{
                  "template_type":"generic",
                  "elements": elements
            }
          } 
        }
      }
      return self.sendMessage(obj)


    
    # feature that is disabled now but will be reactivated in 2021
    def typing(self, sender_id, waiting_time):
      obj1={"recipient": {"id": sender_id}, "sender_action" : "typing_on"}
      res1=self.sendMessage(obj1)
      obj2={"recipient": {"id": sender_id}, "sender_action" : "typing_off"}
      res2=self.sendMessage(obj2)
      return self.sendMessage(obj1)

    #function to notify the user that his message has been received
    # same as typing, it will be reactivated in 2021
    def markSeen(self, sender_id):
      obj1={
        "recipient": {
          "id": sender_id
             },
          "sender_action" : "mark_seen"
          }
      return self.sendMessage(obj1)

    # function to force print information while flask is running
    def log(self, message):
        print(message)
        sys.stdout.flush()



    


