# Track recommender system

As in most cases, when interacting with a chatbot, a user has no information registered about his tastes and I have no dataset nor informations about other user tastes, it is more meaning-ful to build a recommender system based on the similarity between a track he likes and other tracks. So I decided to build a content-based collaborative-filtering recommender system called **More like This** (MLT).




```python
import pandas as pd
import numpy as np
from tqdm import tqdm 
import warnings
warnings.filterwarnings("ignore")
```


```python
tracks=pd.read_csv("datasets/data.csv", sep=',')
```


```python
tracks.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>acousticness</th>
      <th>artists</th>
      <th>danceability</th>
      <th>duration_ms</th>
      <th>energy</th>
      <th>explicit</th>
      <th>id</th>
      <th>instrumentalness</th>
      <th>key</th>
      <th>liveness</th>
      <th>loudness</th>
      <th>mode</th>
      <th>name</th>
      <th>popularity</th>
      <th>release_date</th>
      <th>speechiness</th>
      <th>tempo</th>
      <th>valence</th>
      <th>year</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.991000</td>
      <td>['Mamie Smith']</td>
      <td>0.598</td>
      <td>168333</td>
      <td>0.224</td>
      <td>0</td>
      <td>0cS0A1fUEUd1EW3FcF8AEI</td>
      <td>0.000522</td>
      <td>5</td>
      <td>0.3790</td>
      <td>-12.628</td>
      <td>0</td>
      <td>Keep A Song In Your Soul</td>
      <td>12</td>
      <td>1920</td>
      <td>0.0936</td>
      <td>149.976</td>
      <td>0.6340</td>
      <td>1920</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.643000</td>
      <td>["Screamin' Jay Hawkins"]</td>
      <td>0.852</td>
      <td>150200</td>
      <td>0.517</td>
      <td>0</td>
      <td>0hbkKFIJm7Z05H8Zl9w30f</td>
      <td>0.026400</td>
      <td>5</td>
      <td>0.0809</td>
      <td>-7.261</td>
      <td>0</td>
      <td>I Put A Spell On You</td>
      <td>7</td>
      <td>1920-01-05</td>
      <td>0.0534</td>
      <td>86.889</td>
      <td>0.9500</td>
      <td>1920</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.993000</td>
      <td>['Mamie Smith']</td>
      <td>0.647</td>
      <td>163827</td>
      <td>0.186</td>
      <td>0</td>
      <td>11m7laMUgmOKqI3oYzuhne</td>
      <td>0.000018</td>
      <td>0</td>
      <td>0.5190</td>
      <td>-12.098</td>
      <td>1</td>
      <td>Golfing Papa</td>
      <td>4</td>
      <td>1920</td>
      <td>0.1740</td>
      <td>97.600</td>
      <td>0.6890</td>
      <td>1920</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.000173</td>
      <td>['Oscar Velazquez']</td>
      <td>0.730</td>
      <td>422087</td>
      <td>0.798</td>
      <td>0</td>
      <td>19Lc5SfJJ5O1oaxY0fpwfh</td>
      <td>0.801000</td>
      <td>2</td>
      <td>0.1280</td>
      <td>-7.311</td>
      <td>1</td>
      <td>True House Music - Xavier Santos &amp; Carlos Gomi...</td>
      <td>17</td>
      <td>1920-01-01</td>
      <td>0.0425</td>
      <td>127.997</td>
      <td>0.0422</td>
      <td>1920</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.295000</td>
      <td>['Mixe']</td>
      <td>0.704</td>
      <td>165224</td>
      <td>0.707</td>
      <td>1</td>
      <td>2hJjbsLCytGsnAHfdsLejp</td>
      <td>0.000246</td>
      <td>10</td>
      <td>0.4020</td>
      <td>-6.036</td>
      <td>0</td>
      <td>Xuniverxe</td>
      <td>2</td>
      <td>1920-10-01</td>
      <td>0.0768</td>
      <td>122.076</td>
      <td>0.2990</td>
      <td>1920</td>
    </tr>
  </tbody>
</table>
</div>




```python
tracks.columns
```




    Index(['acousticness', 'artists', 'danceability', 'duration_ms', 'energy',
           'explicit', 'id', 'instrumentalness', 'key', 'liveness', 'loudness',
           'mode', 'name', 'popularity', 'release_date', 'speechiness', 'tempo',
           'valence', 'year'],
          dtype='object')



So the dataset I am using is a dataset from spotify containing feature informations about 170000 tracks and can serve as a good dataset to recommend music to users.

#### Data visualization


```python
# checking missing values
import seaborn as sns
import matplotlib.pyplot as plt



plt.figure(figsize=(20,10))
sns.heatmap(tracks.isna())


```




    <AxesSubplot:>




    
![png](./images/output_8_1.png)
    


No missing values.

##### Visualisation of Variability for each column in the dataframe


```python

fig,ax = plt.subplots(3,4,figsize=(20,15))

sns.distplot(tracks['valence'],ax=ax[0,0])
sns.distplot(tracks['year'],ax=ax[0,1])
sns.distplot(tracks['acousticness'],ax=ax[0,2])
sns.distplot(tracks['danceability'],ax=ax[0,3])
sns.distplot(tracks['energy'],ax=ax[1,0])
sns.distplot(tracks['key'],ax=ax[1,1])
sns.distplot(tracks['liveness'],ax=ax[1,2])
sns.distplot(tracks['loudness'],ax=ax[1,3])
sns.distplot(tracks['popularity'],ax=ax[2,0])
sns.distplot(tracks['speechiness'],ax=ax[2,1])
sns.distplot(tracks['tempo'],ax=ax[2,2])
sns.distplot(tracks['mode'],ax=ax[2,3])
```




    <AxesSubplot:xlabel='mode', ylabel='Density'>




    
![png](./images/output_11_1.png)
    


Here we can see the different distributions for the features in the dataset

###### Characteristics evolutions over the years


```python


columns = ["acousticness","danceability","energy","speechiness","liveness","valence"]
plt.figure(figsize=(30,30))
for c in columns:
    x = tracks.groupby('year')[c].mean()
    sns.lineplot(x.index,x,label=c)
plt.title('Audio characteristics over the years')
plt.xlabel('Year',fontsize=30)
plt.ylabel('Characteristics',fontsize=30)
plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1, prop={'size': 30}, loc = 'upper right')
plt.show()


```


    
![png](./images/output_14_0.png)
    


We can see that the evoluation of the tracks characteristics is pretty interesting, we can see that until the 1970's, the characteristics variate a lot and after the evolution is more stable.

We can also infer from that graphic that even the musical styles changed a lot from 1960, the audio characteristics did not drastically change, so theses parameters are not absolute and music from different styles can have very similar characteristics.

##### Feature selections

As there are a lot of information that are not interesting for the building of the recommender system, I decided to delete the columns :

- Artists -> to many artists to base a similarity on this parameter
- Name -> as the Id is the same that from the API, this is the only identificator needed
- Year and release_date -> these informations are not in the track features sent by the API


```python
df=tracks.copy()
```


```python
df=df.drop(['artists', 'name', 'release_date', 'explicit','year', 'popularity', 'duration_ms'], axis=1)
```


```python
df=df.set_index('id')
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>acousticness</th>
      <th>danceability</th>
      <th>energy</th>
      <th>instrumentalness</th>
      <th>key</th>
      <th>liveness</th>
      <th>loudness</th>
      <th>mode</th>
      <th>speechiness</th>
      <th>tempo</th>
      <th>valence</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0cS0A1fUEUd1EW3FcF8AEI</th>
      <td>0.991000</td>
      <td>0.598</td>
      <td>0.224</td>
      <td>0.000522</td>
      <td>5</td>
      <td>0.3790</td>
      <td>-12.628</td>
      <td>0</td>
      <td>0.0936</td>
      <td>149.976</td>
      <td>0.6340</td>
    </tr>
    <tr>
      <th>0hbkKFIJm7Z05H8Zl9w30f</th>
      <td>0.643000</td>
      <td>0.852</td>
      <td>0.517</td>
      <td>0.026400</td>
      <td>5</td>
      <td>0.0809</td>
      <td>-7.261</td>
      <td>0</td>
      <td>0.0534</td>
      <td>86.889</td>
      <td>0.9500</td>
    </tr>
    <tr>
      <th>11m7laMUgmOKqI3oYzuhne</th>
      <td>0.993000</td>
      <td>0.647</td>
      <td>0.186</td>
      <td>0.000018</td>
      <td>0</td>
      <td>0.5190</td>
      <td>-12.098</td>
      <td>1</td>
      <td>0.1740</td>
      <td>97.600</td>
      <td>0.6890</td>
    </tr>
    <tr>
      <th>19Lc5SfJJ5O1oaxY0fpwfh</th>
      <td>0.000173</td>
      <td>0.730</td>
      <td>0.798</td>
      <td>0.801000</td>
      <td>2</td>
      <td>0.1280</td>
      <td>-7.311</td>
      <td>1</td>
      <td>0.0425</td>
      <td>127.997</td>
      <td>0.0422</td>
    </tr>
    <tr>
      <th>2hJjbsLCytGsnAHfdsLejp</th>
      <td>0.295000</td>
      <td>0.704</td>
      <td>0.707</td>
      <td>0.000246</td>
      <td>10</td>
      <td>0.4020</td>
      <td>-6.036</td>
      <td>0</td>
      <td>0.0768</td>
      <td>122.076</td>
      <td>0.2990</td>
    </tr>
  </tbody>
</table>
</div>



To build a simple MLT system, I just need to compute the similarity between a given track and all the tracks in the database and return the most similars.

To do so I need to implement a similarity function between two tracks, for that I decided to use the cosine similarity.

First, to compute the cosine similarity, I need to normalize the data. In order to do so I will use a mean normalization


```python
#normalized_df=(df-df.mean())/df.std()
normalized_df=(df-df.min())/(df.max()-df.min())
```


```python
normalized_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>acousticness</th>
      <th>danceability</th>
      <th>energy</th>
      <th>instrumentalness</th>
      <th>key</th>
      <th>liveness</th>
      <th>loudness</th>
      <th>mode</th>
      <th>speechiness</th>
      <th>tempo</th>
      <th>valence</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0cS0A1fUEUd1EW3FcF8AEI</th>
      <td>0.994980</td>
      <td>0.605263</td>
      <td>0.224</td>
      <td>0.000522</td>
      <td>0.454545</td>
      <td>0.3790</td>
      <td>0.741868</td>
      <td>0.0</td>
      <td>0.096395</td>
      <td>0.615900</td>
      <td>0.6340</td>
    </tr>
    <tr>
      <th>0hbkKFIJm7Z05H8Zl9w30f</th>
      <td>0.645582</td>
      <td>0.862348</td>
      <td>0.517</td>
      <td>0.026400</td>
      <td>0.454545</td>
      <td>0.0809</td>
      <td>0.825918</td>
      <td>0.0</td>
      <td>0.054995</td>
      <td>0.356823</td>
      <td>0.9500</td>
    </tr>
    <tr>
      <th>11m7laMUgmOKqI3oYzuhne</th>
      <td>0.996988</td>
      <td>0.654858</td>
      <td>0.186</td>
      <td>0.000018</td>
      <td>0.000000</td>
      <td>0.5190</td>
      <td>0.750168</td>
      <td>1.0</td>
      <td>0.179197</td>
      <td>0.400810</td>
      <td>0.6890</td>
    </tr>
    <tr>
      <th>19Lc5SfJJ5O1oaxY0fpwfh</th>
      <td>0.000174</td>
      <td>0.738866</td>
      <td>0.798</td>
      <td>0.801000</td>
      <td>0.181818</td>
      <td>0.1280</td>
      <td>0.825135</td>
      <td>1.0</td>
      <td>0.043769</td>
      <td>0.525640</td>
      <td>0.0422</td>
    </tr>
    <tr>
      <th>2hJjbsLCytGsnAHfdsLejp</th>
      <td>0.296185</td>
      <td>0.712551</td>
      <td>0.707</td>
      <td>0.000246</td>
      <td>0.909091</td>
      <td>0.4020</td>
      <td>0.845102</td>
      <td>0.0</td>
      <td>0.079094</td>
      <td>0.501324</td>
      <td>0.2990</td>
    </tr>
  </tbody>
</table>
</div>




```python
import math
def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    if sumxx*sumyy != 0:
        return sumxy/math.sqrt(sumxx*sumyy)
    else:
        return 0
```


```python

track1 = normalized_df.iloc[4,:]
track2 = normalized_df.iloc[22, :]

print(cosine_similarity(list(track1), list(track2)))
```

    0.6065626516117105
    

Here we can see the data is normalized we can now compute our cosine similarity. To build our recommender system, we will simply 


```python

def get_recommendations(track_vector, track_matrix, N):
    # track vector is the given track vector we want to find similar tracks with
    # N is number of similar tracks returned
    res={}
    # compute the similarity for each track of the dataset
    for trackId, track in track_matrix.iterrows():
        # as we don't want to return the same track 
        res[trackId]=cosine_similarity(list(track_vector), list(track))
    #sort the result
    res=dict(sorted(res.items(), key=lambda res: res[1], reverse=True)[:N])
    return res             


```


```python
recommendations=get_recommendations(track1, normalized_df, 2)
```


```python
def displayResults(recommendations):
    for id, score in recommendations.items():
        track=tracks.loc[tracks['id']==id]
        name=track['name'].values[0]
        artists=track['artists'].values
        print('Title : {}, artists : {}, score : {}'.format(name, artists, score))
```


```python
displayResults(recommendations)
```

    Title : Xuniverxe, artists : ["['Mixe']"], score : 1.0
    Title : Harold the Barrel, artists : ["['Genesis']"], score : 0.9975424470398455
    

By listening to the song, we can see that they are not similar at all, there are a lot of ameliorations to compute with the recommender system. But that was just a test, we didn't even cluster the data. 

As tracks from very different genres can have the same characteristics, it could be interesting to cluster the songs taking in account this feature to add a new feature to our tracks

### Clustering


```python
data=normalized_df.copy()
```


```python
from sklearn.cluster import KMeans

km=KMeans(n_clusters=10)
category=km.fit_predict(normalized_df)
normalized_df['category']=category
normalized_df['category']=(normalized_df['category'] - normalized_df['category'].min())/(normalized_df['category'].max() - normalized_df['category'].min())
```


```python
# as the normalized categories are in the same order, we store them in a list
# and will use the index+1 (as index begins at 0) to get the corresponding category non-normalized
normalize_categories=list(normalized_df['category'].unique())
normalize_categories.sort()
```

Now that we know how to get the cluster for an unknown vector, we can try to get the recommendations

As the cosine similarity was not really this accurate (similarity close to 1 for songs completely different) I decided to compute the Manhattan Distance that is more focus on each different feature precisely.


```python
def get_recommendations_2(track, tracksDf, N=1):
    #track is a vector of all selected characteristics 
    song=tracks.loc[tracks['id']==track.name]
    print('Getting recommendations for {} by {} '.format(song["name"].values[0], song.artists.values[0]))
    res={}
    res[track.name]=1000
    for trackId, otherTrack in tracksDf.iterrows():
        dist=0
        for col in np.arange(len(tracksDf.columns)):
            # manhattan distance
            dist=dist+np.absolute(float(track[col]) - float(otherTrack[col]))
        res[trackId]=dist
    # sorting by ascending order as we computed distance and not similarity
    res=dict(sorted(res.items(), key=lambda res: res[1])[1:N]) #we do not take the first value that is the same song
    displayResults(res) 
```


```python
track_test=normalized_df.iloc[13,:]
recommendations=get_recommendations_2(track_test,normalized_df, 5)
```

    Getting recommendations for Schumacher by ['Justrock'] 
    Title : Gottlos, artists : ["['Agonoize']"], score : 0.3599554771209725
    Title : It Makes Me Sick - Demo August 2011, artists : ["['Joy/Disaster']"], score : 0.36606696163803903
    Title : Praise You - Radio Edit, artists : ["['Fatboy Slim']"], score : 0.38075408010043077
    Title : Breakout, artists : ["['Bon Jovi']"], score : 0.43639366765550813
    

### Model precision

It could be interesting to compare different type of distances and try to see which one is the best. There are two aspect to test : 

- First the pertinence of the items returned as we want our system to give the user good items
- Then, the time to compute, as the messenger API expects a response within 20sec, we need to work out this point.

Also, as the system will be integrated with a class in the main code, it could be good to adapt the recommendations in a class object from now on.


```python
from math import *
# class to syntethize and integrate the work done on the notebook
class recommender():

    def __init__(self):
        self.tracks=pd.read_csv("datasets/data.csv", sep=',')
        self.normalized_tracks, self.km = self.preprocessing(self.tracks)
        self.normalize_clusters=list(self.normalized_tracks['cluster'].unique()).sort()
    
    # euclidian_distance between 2 vectors
    def euclidean_distance(self, x,y):
         return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))
        
    # manhattan distance between 2 vectors
    def manhattan_distance(self, x, y):
        return sum(abs(a-b) for a,b in zip(x,y))
    
    # synthetise the preprocessing steps in one function
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

            
    def get_recommendation_euclidian(self, track_name, N):
        track = self.tracks[(self.tracks['name'].str.lower() == track_name.lower())].head(1)
        if track is not None:
      # if track found in the dataset getting the vector associated
            track_vector=self.normalized_tracks.loc[track['id'].values[0], :]
            res={}
            for trackId, otherTrack in tqdm(self.normalized_tracks.iterrows()):
                dist=self.euclidean_distance(list(track_vector), list(otherTrack))
                res[trackId]=dist
    # sorting by ascending order as we computed distance and not similarity
            res=dict(sorted(res.items(), key=lambda res: res[1])[1:N]) #we do not take the first value that is the same song
            return res
        else:
              return None
            
    def get_recommendation_manhattan(self, track_name, N):
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
            
    def displayResults(self, recommendations):
        for id, score in recommendations.items():
            track=tracks.loc[tracks['id']==id]
            name=track['name'].values[0]
            artists=track['artists'].values
            print('Title : {}, artists : {}, score : {}'.format(name, artists, score))
    

  
```


```python
recom=recommender()
```


```python
res=recom.get_recommendation_manhattan('Billie Jean', 5)
displayResults(res)
```

    174389it [00:08, 20800.42it/s]
    

    Title : Billie Jean, artists : ["['Michael Jackson']"], score : 0.1741409337938068
    Title : I Want You, artists : ["['Gary Low']"], score : 0.24962034485312506
    Title : Move Ya Body, artists : ["['Nina Sky', 'Jabba']"], score : 0.24993882106425594
    Title : Misty Morning - Kaya 40 Mix, artists : ["['Bob Marley & The Wailers', 'Stephen Marley']"], score : 0.27252539621328287
    


```python
res=recom.get_recommendation_euclidian('Billie Jean', 5)
displayResults(res)
```

    174389it [00:09, 18294.63it/s]
    

    Title : Billie Jean, artists : ["['Michael Jackson']"], score : 0.09308961526539382
    Title : Move Ya Body, artists : ["['Nina Sky', 'Jabba']"], score : 0.10216686580844991
    Title : Misty Morning - Kaya 40 Mix, artists : ["['Bob Marley & The Wailers', 'Stephen Marley']"], score : 0.1200671324764336
    Title : I Want You, artists : ["['Gary Low']"], score : 0.12693858680567838
    

The mannhattan and the euclidian distances returns pretty similar items, but the manhattan is a little faster, so I decided to keep it to integrate it in my model.
