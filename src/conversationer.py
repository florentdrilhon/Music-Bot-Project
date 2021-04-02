# class to respond back to the user according to its intent
import random
from recommender.recommender import recommender
import time

class conversationer():

  def __init__(self, spotiConnector, fbeamer ):

      #spotiConnector is an instance from the class spotifyConnector
      # allowing the conversationer to interact with the API
      self.spotiConnector=spotiConnector
      self.fb=fbeamer
      self.recom = recommender()
      self.state= {'lastTrack': None, 'lastArtist': None}

      # patterns contain response templates to send the user
      self.patterns={}
      self.patterns['hello']=["Hello there !", "Hi, nice to meet you", "Hi there"]
      self.patterns['actions']=["What can I do for you ?", "Is there something you want to ask me ?", "What do you want me to do ?"]
      self.patterns["Thank you"]=["You're welcome 😊", "It's my pleasure 😉", "Always here to answer questions from a passionate ! 😉"]
      self.patterns["presentation"]=["I'm Fabrice, a bot designed to answer questions about music (especially tracks and artist) and give recommendations about the same topic, so please try to ask me a question about a music 😄"]
      self.patterns["non-understanding"]=["Sorry I didn't understand your question, please try again 😅", "I apologize but I did not undersant your request, please send it again 😅", "Pardon me, I am a young bot and I did not understand your meaning, do not hesitate to try again and I'll try to make progress !😅"]
      self.patterns["Goodbye"]=["See you around 😉!", "Have a nice day !", "It was a pleasure to answer your questions, see you another time !"]
      self.patterns["listen"]=["You can listen on the Spotify platform here 👉", "Check it out here 👉", "Follow this link to listen to this item 👉", "If you to listen to this track, just click here 👉"]
      self.patterns["image"]=["Here is a little picture to illustrate 😉", "For your eyes only 😎", "To make your eyes meet your ears 😋"]
      self.patterns["recommendations"]=["Here are some items that you may like 🎶", "I found some other items that can interest you 😉", "Check out those recommendations I got four you 👌"]

      # TODO ajouter des patterns



  def hello(self, senderId):
    # select answer random from the templates
    answer=random.choices(self.patterns['hello'])[0]
    self.fb.typing(senderId,1)
    time.sleep(1)
    self.fb.txtSender(senderId, answer )
    answer=random.choices(self.patterns['actions'])[0]
    self.fb.typing(senderId,3)
    time.sleep(3)
    self.fb.txtSender(senderId, answer )


  def goodBye(self, senderId):
    answer=random.choices(self.patterns['Goodbye'])[0]
    self.fb.txtSender(senderId, answer )



  # TODO check ce scénario

  def trackInfo(self, message):
    # getting the information about the asked track
    trackName=self.fb.extractEntity(message["nlp"], "track:track")
    if trackName:
      track=self.spotiConnector.searchTrack(trackName)
      # setting answer with main informations
      answer="{} is a track made by {} from the {} {} released in {}".format(track["name"], track["artist"]["name"], track["album"]["type"], track["album"]["name"], track["album"]["release"])
      self.fb.txtSender(message["senderId"], answer)
      time.sleep(2)
      answer=random.choices(self.patterns['listen'])[0]
      self.fb.txtSender(message["senderId"], answer)
      time.sleep(1.5)
      self.fb.trackSender(message["senderId"], [track])
      time.sleep(5)
      self.state["lastTrack"]=track
      self.fb.quickReplies(message["senderId"], "Did you like this track ?", "Yes ! 👍", "Not much 👎")
    else : 
      self.fb.txtSender(message["senderId"], "Sorry I couldn't understand the name of the track you're looking for 😓")



  def trackRecommendations(self,senderId, track):
      # getting recommendations and keeping in memory knowntracks to check for doublons
      recommendations=self.recom.get_recommendation(track["name"])
      knownTracks=[track] 
      if recommendations is not None:
        self.fb.txtSender(senderId, random.choices(self.patterns['recommendations'])[0])
        i, j = 0, 0
        # as we want to recommend exactly 3 songs
        while i < 3 : 
          id=list(recommendations.keys())[j]
          recommendedTrack=self.spotiConnector.searchTrack(id=id)
          if self.recom.isDoublon(recommendedTrack, knownTracks)== False:
            knownTracks.append(recommendedTrack)
            i+=1
          j+=1
        # sending the identified tracks in a carrousel
        self.fb.trackSender(senderId, knownTracks[1:])
      # no recommendations found
      else :
        self.fb.txtSender(senderId, "Sorry I could not find recommendations for you track 😔")


  # gives information about an asked artist
  def artistInfo(self, message):
      artistName=self.fb.extractEntity(message["nlp"], "artist:artist")
      if artistName:
        artist=self.spotiConnector.searchArtist(artistName)
        # setting answer with main informations
        answer="{} is a {} artist".format(artist["name"],artist["genres"][0])
        self.fb.txtSender(message["senderId"], answer)
        self.fb.artistSender(message["senderId"], [artist])
        # save artist in the state for the next scenarii
        self.state["lastArtist"]=artist
        self.fb.quickReplies(message["senderId"], "You like this artist ?", "Artist best tracks 🎶", "Related Artists 🎤")
      else : 
        self.fb.txtSender(message["senderId"], "Sorry I couldn't understand the name of the artist you're looking for 😓")


  # get the artist who made a asked song
  def getArtist(self, message):
    # getting the information about the asked track
    trackName=self.fb.extractEntity(message["nlp"], "track:track")
    if trackName:
      track=self.spotiConnector.searchTrack(trackName)
      # setting answer with main informations
      answer="{} was composed by {}".format(track["name"], track["artist"]["name"])
      self.fb.txtSender(message["senderId"], answer)
      time.sleep(2)
      answer=random.choices(self.patterns['listen'])[0]
      self.fb.txtSender(message["senderId"], answer)
      time.sleep(1.5)
      self.fb.txtSender(message["senderId"], track["link"])
      time.sleep(5)
      self.state["lastTrack"]=track
      self.fb.quickReplies(message["senderId"], "Do you like this track ?", "Yes ! 👍", "Not much 👎")
    else : 
      self.fb.txtSender(message["senderId"], "Sorry I couldn't understand the name of the track you're looking for 😓")


  def artistBestTracks(self, message):
    # check if an artist is in the state
    # if not, try to get if from the message
    artist=None
    if self.state["lastArtist"] is None:
      artistName=self.fb.extractEntity(message["nlp"], "artist:artist")
      if artistName:
        artist=self.spotiConnector.searchArtist(artistName)
    else :
      artist=self.state["lastArtist"]
    if artist is not None:
      answer= "Here are the best tracks of {} 🤘".format(artist["name"])
      self.fb.txtSender(message["senderId"], answer)
      self.fb.trackSender(message["senderId"],artist['top tracks'] )
    else:
      self.fb.txtSender(message["senderId"], "Sorry I couldn't understand the name of the artist 😔")


  # send artist's related artists
  def relatedArtists(self, message):
    # checking if an artists is registered in the state
    if self.state["lastArtist"] is not None:
      # send his related artists
      answer="Here are artists close to {} 🎤".format(self.state["lastArtist"]["name"])
      self.fb.txtSender(message["senderId"], answer)
      relatedArtists=self.state["lastArtist"]["related artists"]
      self.fb.artistSender(message["senderId"], relatedArtists)
    else :
      # notify the user 
      self.fb.txtSender(message["senderId"], "Sorry, I could not remember the artist we are talking about 😓")
    


  def main(self,message):
    self.fb.log('\nSending response\n')
    if message['intent'] is None:
      answer=random.choices(self.patterns['non-understanding'])[0]
      self.fb.txtSender(message['senderId'], answer )

    if message['intent']=='Hello':
      self.hello(message['senderId'])

    if message['intent']=='Goodbye':
      self.goodBye(message['senderId'])

    if message['intent']=='Thank_you':
      answer=random.choices(self.patterns['Thank you'])[0]
      self.fb.txtSender(message['senderId'], answer )

    if message['intent']=='presentation':
      answer=random.choices(self.patterns['presentation'])[0]
      self.fb.txtSender(message['senderId'], answer )

    if message['intent']=='trackInfo':
      self.trackInfo(message)

    if message['intent']=='artistInfo':
      self.artistInfo(message)
    
    if message['intent']=='getArtist':
      self.getArtist(message)

    if message['intent']=='artistsBestTracks':
      self.artistBestTracks(message)

    if message['intent']=='relatedArtists':
      self.relatedArtists(message)

    if message['intent']=='yes':
      #the user wants to get recommendations
      if self.state["lastTrack"]:
          self.trackRecommendations(message["senderId"],self.state["lastTrack"])
    if message['intent']=='No':
      self.state['lastTrack']=None
      self.fb.txtSender(message["senderId"], "Sorry that you didn't like it 😔")
  
  # TODO fonction qui prend en entrée une un objet message (contenant intent + entités) et lançant le scénario associé

