import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class spotifyConnector():
    
  def __init__(self, cid, secret):
      # initialising the connector with the required information
    self.cid=cid #client ID
    self.secret = secret #secret ID
    self.client_credentials_manager=SpotifyClientCredentials(cid, secret)
    self.sp=spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)


  # function to search an item (any type) in order to return its ID
  # to make a more detailed search with the ID

  # get main information about an album in the answer made by the spotify API
  def extractAlbumInfo(self, albumObject):
    id=albumObject["id"]
    name=albumObject["name"]
    release=albumObject["release_date"]
    type=albumObject["type"]
    return {'id': id, 'name': name, 'release': release, 'type': type}

  
  # get main info about a track given a trackObject from the Spotify api
  def extractTrackInfo(self, trackObject):
    obj={}
    # getting main information about the track
    obj["artist"]=trackObject["album"]["artists"][0]
    obj["id"]=trackObject["id"]
    obj["name"]=trackObject["name"]
    obj["link"]=trackObject["external_urls"]["spotify"]
    obj["album"]=self.extractAlbumInfo(trackObject["album"])
    obj["track_features"]=None
    # getting details about track feature 
    if obj["id"] :
      trackdetails=self.sp.audio_features(obj["id"])
      obj["track_features"]=trackdetails
    return obj

  # TODO transform the function to get only ID of queried item
  def searchTrack(self, trackName=None, id=None):
    if id is not None :
      track=self.sp.track(id)
    else:
      results=self.sp.search(q=trackName, limit=1, type='track')
      track=results["tracks"]["items"][0]
    track=self.extractTrackInfo(track)
    return track


  

  # TODO get track info with its ID

  def searchArtist(self, artistName, ):
    result = self.sp.search(q=artistName, limit=1, type='artist')
    artist=result["artists"]["items"][0]
    # extracting main information about an artist
    obj={}
    obj["name"]=artist["name"]
    obj["popularity"]=artist["popularity"]
    obj["id"]=artist["id"]
    obj["link"]=artist["external_urls"]["spotify"]
    obj["genres"]=artist["genres"]
    obj["image"]=artist["images"][0]["url"]
    # getting the top tracks of this artist
    top_tracks=self.sp.artist_top_tracks(obj["id"], country="FR")["tracks"][:3]
    top_tracks= [self.extractTrackInfo(track) for track in top_tracks]
    obj["top tracks"]=top_tracks
    return obj




  # TODO get artist info with its ID

  # TODO BONUS get album info with its ID

