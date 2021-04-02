import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class spotifyConnector():
    
  def __init__(self, cid, secret):
      # initialising the connector with the required information
    self.cid=cid #client ID
    self.secret = secret #secret ID
    self.client_credentials_manager=SpotifyClientCredentials(cid, secret)
    self.sp=spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)


  # get main information about an album object from the spotify API
  def extractAlbumInfo(self, albumObject):
    id=albumObject["id"]
    name=albumObject["name"]
    release=albumObject["release_date"]
    albumType=albumObject["type"]
    image=albumObject["images"][0]["url"]
    return {'id': id, 'name': name, 'release': release, 'type': albumType, 'image': image}

  
  # get main info about a track given a trackObject from the Spotify API
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

  #function to extract artists main info from an artist object sent by the API
  def extractArtistsInfo(self, artistObject):
    obj={}
    obj["name"]=artistObject["name"]
    obj["popularity"]=artistObject["popularity"]
    obj["id"]=artistObject["id"]
    obj["link"]=artistObject["external_urls"]["spotify"]
    obj["genres"]=artistObject["genres"]
    obj["image"]=artistObject["images"][0]["url"]
    return obj

  
  # function to get a track info from a given track name
  def searchTrack(self, trackName=None, id=None):
    if id is not None :
      track=self.sp.track(id)
    else:
      results=self.sp.search(q=trackName, limit=1, type='track')
      track=results["tracks"]["items"][0]
    track=self.extractTrackInfo(track)
    return track


  # function to get a track info from a given artist name
  def searchArtist(self, artistName ):
    result = self.sp.search(q=artistName, limit=1, type='artist')
    artist=result["artists"]["items"][0]
    # extracting main information about an artist
    obj=self.extractArtistsInfo(artist)
    # getting the top tracks of this artist
    top_tracks=self.sp.artist_top_tracks(obj["id"], country="FR")["tracks"][:3]
    top_tracks= [self.extractTrackInfo(track) for track in top_tracks]
    #getting related artists
    relatedArtists=self.sp.artist_related_artists(obj["id"])["artists"][:3]
    relatedArtists= [self.extractArtistsInfo(artist) for artist in relatedArtists]
    obj["top tracks"]=top_tracks
    obj["related artists"]=relatedArtists
    return obj


