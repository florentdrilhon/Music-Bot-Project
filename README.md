# Music Advice Bot

A bot to answer questions about music, but also with a recommender sytem to propose new musics for the user to like.

Bot facebook dev link : https://developers.facebook.com/apps/267113828326789/messenger/settings/

- language : python -> easier to integrate the recommender system to the bot
- platform : messenger -> good python library to create such a bot
- Bot based on AI-rule with wit.ai
- recommender system in python too
- obtain the data with deezer API : https://rapidapi.com/deezerdevs/api/deezer-1


The bot can answer questions about music and tracks using the Spotify web API and then use theses researches to recommend music to the user.


Recommender system :

To recommend items to the user, as the user is not known by the system at first, I decided to use a collaborative filtering content-based recommender system.

I found a a Spotify dataset based on Tracks and artist, so I was able to create clusters among those data. So when a user asks questions about a track or an artist, I get the related information and predict the cluster to which belongs this info and return the most similar items (tracks or artist) and send them back to the user.

- recommend to the user a track he might like based on his researches
- recommend an artist to the user based on his researches