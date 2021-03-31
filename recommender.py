import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from tqdm import tqdm
from math import *

# class to syntethize and integrate the work done on the notebook
class recommender():

  def __init__(self):
    self.tracks=pd.read_csv("recommender/datasets/data.csv", sep=',')
    self.normalized_tracks, self.km = self.preprocessing(self.tracks)
    self.normalize_clusters=list(self.normalized_tracks['cluster'].unique()).sort()

  def manhattan_distance(self, x, y):
        return sum(abs(a-b) for a,b in zip(x,y))


  def preprocessing(self,df):
    # to gather all the preprocessing steps in one function
    # deleting unwanted features
    df=df.drop(['artists', 'name', 'release_date', 'explicit','year', 'popularity', 'duration_ms'], axis=1)
    df=df.set_index('id')
    #normalize 
    df=(df-df.min())/(df.max()-df.min())
    # clustering
    km=KMeans(n_clusters=10)
    cluster=km.fit_predict(df)
    df['cluster']=cluster
    df['cluster']=(df['cluster'] - df['cluster'].min())/(df['cluster'].max() - df['cluster'].min())
    return df, km

  # get the cluster for a track not in the dataset
  def get_cluster(self, track):
    track=pd.DataFrame(track)
    cluster=self.km.predict(track)
    cluster=self.normalize_clusters[cluster[0]-1] #getting the normalized cluster
    track['cluster']=cluster
    return track

  def get_recommendation(self, track_name, N):
    track = self.tracks[(self.tracks['name'].str.lower() == track_name.lower())].head(1)
    if track is not None:
      # if track found in the dataset getting the vector associated
      track_vector=self.normalized_tracks.loc[track['id'].values[0], :]
      res={}
      for trackId, otherTrack in tqdm(self.normalized_tracks.iterrows()):
        dist=self.manhattan_distance(list(track_vector), list(otherTrack))
        res[trackId]=dist
    # sorting by ascending order as we computed distance and not similarity
      res=dict(sorted(res.items(), key=lambda res: res[1])[1:N]) #we do not take the first value that is the same song
      return res
    else:
      return None
    

  