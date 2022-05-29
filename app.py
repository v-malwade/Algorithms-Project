from random import choices
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")
import recommendation_algoritms as algo

st.set_page_config(page_title="Song Recommendation", layout="wide")

def get_choices(list):
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        choices = []
        x = int((len(list))/4)+1
        for i in range(0,x):
            if(col1.checkbox(list[i])):
                choices.append(list[i])
        for i in range(x,x*2):
            if(col2.checkbox(list[i])):
                choices.append(list[i])
        for i in range(x*2,x*3):
            if(col3.checkbox(list[i])):
                choices.append(list[i])
        for i in range(x*3,min(len(list),x*4)):
            if(col4.checkbox(list[i])):
                choices.append(list[i])
    return choices

def show_tracks(uris):
    list = []
    for uri in uris:
        track = """<iframe src="https://open.spotify.com/embed/track/{}" width="260" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(uri)
        list.append(track)
    col1, col2, col3, col4 = st.columns(4)
    x = int((len(list))/4)
    for i in range(0,x):
        with col1:
            components.html(list[i], height=350,width=300)
    for i in range(x,x*2):
        with col2:
            components.html(list[i], height=350,width=300)
    for i in range(x*2,x*3):
        with col3:
            components.html(list[i], height=350,width=300)
    for i in range(x*3,min(len(list),x*4)):
        with col4:
            components.html(list[i], height=350,width=300)

def page():
    title = "Song Recommendation Engine"
    st.title(title)
    st.title("Hey User")

    col1, col3, col2 = st.columns([5,1,5])    
    user = col1.text_input("Name: ")
    gender_values = ["Female", "Male", " Other", " Do not prefer to disclose"]
    gender = col2.radio("Gender: ",gender_values)
    age = col1.text_input('Age', '18')
    dob = 2022-int (age)

    df = algo.load_data() 
    df = df.drop_duplicates(subset='id', keep="first")
    user_list =  pd.read_csv("user_list.csv")
    user_list = user_list.sort_values(by="frequency",ascending=False)

    artists_choice = ['AC/DC', 'Adele', 'Ariana Grande', 'Avicii', 'Beyoncé', 'Bruno Mars', 'Calvin Harris', 'Camila Cabello',
            'Coldplay', 'Daddy Yankee', 'David Guetta', 'Dua Lipa', 'Ed Sheeran', 'Green Day', 'Katy Perry', 'Kendrick Lamar',
            'Martin Garrix', 'Metallica', 'Migos', 'Nicky Jam', 'One Direction', 'Pink Floyd', 'Queen',
            'Red Hot Chili Peppers', 'Shakira', 'Sia', 'The Chainsmokers', 'Twenty One Pilots']
    st.write('Select atists:')
    artists = get_choices(artists_choice)

    genre_names = ['Dance Pop', 'Electronic', 'Electropop', 'Hip Hop', 'Jazz', 'K-pop', 'Latin', 'Pop', 'Pop Rap', 'R&B', 'Rock']
    st.write('Select genre:')
    genre = get_choices(genre_names)
    genre = [x.lower() for x in genre]
    audio_feats = ["acousticness", "danceability", "energy", "instrumentalness", "valence", "tempo"]
    metrices = algo.calculate_metrices(df,user_list)
    st.markdown("")
    if st.button("Get Recommendations"):   
        st.title("Recommended for you")
        uris, audios = algo.recommended_for_you(df, genre, artists, dob, metrices)
        uris = uris[:20]    
        show_tracks(uris)

        st.title("Find your new Favourite Song")
        uris, audios = algo.find_new_fav(df, user_list,genre, artists, dob, metrices)
        uris = uris[:20] 
        show_tracks(uris)

        st.title("More like you Favourite Artist")
        uris, audios, fav_artists = algo.top_artist(df, user_list, genre, artists, dob, metrices)
        st.markdown("You top 2 artists are:")
        st.markdown(fav_artists[0])  
        st.markdown(fav_artists[1])  
        show_tracks(uris)

        st.title("Your Top Mixes")
        uris= algo.top_mixes(df, user_list)  
        show_tracks(uris)


def main():
    page()

if __name__=='__main__':
    main()
