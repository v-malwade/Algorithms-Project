import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

def load_data():
    df = pd.read_csv("processed_data.csv")
    df['genres'] = df.genres.apply(lambda x: [i[1:-1] for i in str(x)[1:-1].split(", ")])
    df = df.explode("genres")
    return df

def get_songs(data, genre, artists, start_year,n, metrices):
    audio_feats = ["acousticness", "danceability", "energy", "instrumentalness", "valence", "tempo"]
    neigh = NearestNeighbors()
    neigh.fit(data[audio_feats].to_numpy())
    n_neighbors = neigh.kneighbors([metrices], n_neighbors=len(data), return_distance=False)[0]

    uris = data.iloc[n_neighbors]["uri"].tolist()
    audios = data.iloc[n_neighbors][audio_feats].to_numpy()
    return uris, audios

def recommended_for_you(df, genre, artists, start_year, metrices):
    data = df[(df["genres"].isin(genre)) & (df["artists_name"].isin(artists)) & (df["release_year"]>=start_year)]
    data = data.sort_values(by='popularity', ascending=False)[:1000]

    uris, audios = get_songs(data, genre, artists, start_year, 20, metrices)
    return uris, audios

def top_artist(df, user_list, genre, artists, start_year, metrices):
    uris = user_list['uri'].tolist()
    data = df[(df["uri"].isin(uris))]
    artists = data['artists_name'].value_counts()[:2].index.tolist()
    data = data[(data["artists_name"].isin(artists))]
    data = data.sort_values(by='popularity', ascending=False)[:500]
    uris, audios = get_songs(data, genre, artists, start_year, 20, metrices)
    return uris, audios, artists

def top_mixes(df,user_list):
    uris = user_list['uri'].tolist()
    return uris[:10]

def find_new_fav(df,user_list,genre, artists, start_year, metrices):
    data = df[(df["genres"].isin(genre))]
    data = data.sort_values(by='popularity', ascending=False)[:800]
    
    uris, audios = get_songs(data, genre, artists, start_year,30, metrices)
    return uris, audios

def calculate_metrices(df,user_list):
    uris = user_list['uri'].tolist()
    audio_feats = ["acousticness", "danceability", "energy", "instrumentalness", "valence", "tempo"]
    data = df[(df["uri"].isin(uris))]
    metrices = np.array(data[audio_feats].mean())
    return metrices
    
    
def main():
    df = load_data() 
    df = df.drop_duplicates(subset='id', keep="first")
    user_list =  pd.read_csv("user_list.csv")
    user_list.sort_values(by="frequency",ascending=False)

if __name__ == "__main__":
    main()