# Music Advice Bot

A bot to answer questions about music, but also with a recommender sytem to propose new musics for the user to like.

Bot facebook dev link : https://developers.facebook.com/apps/267113828326789/messenger/settings/

- language : python -> easier to integrate the recommender system to the bot
- platform : messenger -> good python library to create such a bot
- Bot based on AI-rule with wit.ai
- recommender system in python too
- obtain the data with deezer API : https://rapidapi.com/deezerdevs/api/deezer-1


The bot can answer questions about music and tracks using the Spotify web API and then use theses researches to recommend music to the user.


### Intents and scenariis:

All the intents and scenarii are detailed in the conversationner.py. It contains a class that is used to handle all the thread of the conversation, launch scenarii and give different responses.

##### Patterns

The conversationner class has a property "patterns" that is a dictionnary in which I precised different answer model for a given situation (as key in the dict).


##### Basic scenarii

The bot is able to detect Hello/Goodbye/Thanks/Presentation/ intents and answer it accordingly, and it also gives a suitable answer when it doesn't understand the intent or other things. 

##### Give informations about tracks

Try asking "tell me about the song/track <trackName> and the bot will provide you basic informations about the asked track

Then it will ask you if you liked the track and trigger the recommendation scenario if yes. 

##### Recommendations

The scenario use an object from the recommender class, it gives it as argument the last track sent to the user, (kept in memory in the state property) and try to compute the recommendations to give back the user 3 tracks he may like.


##### Artist Info

Must precise the word "Singer/group/artist" for the bot to understant that the user does not asks for a track (NLP engine are not this accurate nowadays unfotunately).
The bot then sends informations about the artist, an image an the link of the best artist track.


##### Gives artist who made a precise track

Gives the user the artist who made an asked track and ask him if he like this track.

If yes, send him recommendations.

##### Artist's Related artists

Triggered after the artistInfo scenario. Sends to the user the related Artists of the last artist the user asked about. The bot send the 3 artists in a caroussel of 3 artist templates.

##### Artist's Best tracks

Triggered after the artistInfo scenario. Sends to the user the 3 best tracks of the last artist the user asked about. Again it send it in a carrouseel of 3 tracks templates.


## Recommender system :

To recommend items to the user, as the user is not known by the system at first, I decided to use a collaborative filtering content-based recommender system.

I found a a Spotify dataset based on Tracks and artist, so I was able to create clusters among those data. So when a user asks questions about a track or an artist, I get the related information and predict the cluster to which belongs this info and return the most similar items (tracks or artist) and send them back to the user.

- recommend to the user a track he might like based on his researches
- recommend an artist to the user based on his researches