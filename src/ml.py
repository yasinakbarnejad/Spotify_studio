import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def get_genre_average(df):
    genre_average = df.groupby('track_genre')['popularity'].agg(avg_popularity='mean').round(2).sort_values("avg_popularity", ascending=False).reset_index()
    return genre_average

def get_artist_average(df):
    df['artist'] = df['artists'].str.split(';')
    separated_df = df.explode('artist')
    separated_df['artist'] = separated_df['artist'].str.strip()
    artist_stat = separated_df.groupby("artist")["popularity"].agg(
        avg_popularity="mean", 
        hits=lambda x: (x > 50).sum(),
        count="count").sort_values("avg_popularity", ascending=False).reset_index()
    return artist_stat

def prepare_features(df):
    genre_mean = get_genre_average(df)
    genre_mean_dict = genre_mean.set_index('track_genre')['avg_popularity'].to_dict()
    
    artist_mean = get_artist_average(df)
    artist_mean_dict = artist_mean.set_index('artist')['avg_popularity'].to_dict()
    median_artist = artist_mean['avg_popularity'].median()
    
    analysis_df = df.copy()
    analysis_df['genre_mean'] = df['track_genre'].map(genre_mean_dict)
    analysis_df['energy*Instrumentalness'] = df['instrumentalness'] *df['energy']
    analysis_df['acousticness^2'] = df['acousticness']**2
    analysis_df['valence^2'] = df['valence']**2
    
    songs_exploded = df.assign(artist_split=df['artists'].str.split(';')).explode('artist_split')
    songs_exploded['artist_mean'] = songs_exploded['artist_split'].map(artist_mean_dict)
    songs_exploded['artist_mean'] = songs_exploded['artist_mean'].fillna(median_artist)
    analysis_df['artist_mean'] = songs_exploded.groupby(songs_exploded.index)['artist_mean'].mean()
    
    return analysis_df, genre_mean_dict, artist_mean_dict, median_artist

def train_models(df):
    analysis_df, genre_mean_dict, artist_mean_dict, median_artist = prepare_features(df)
    
    full_features = ["artist_mean", "energy*Instrumentalness", "acousticness^2", 
                     "valence^2", "genre_mean", "loudness"]
    genre_artist_features = ["genre_mean", "artist_mean"]
    artist_features = ["artist_mean", "energy*Instrumentalness"]
    genre_features = ["genre_mean", "energy*Instrumentalness"]
    weak_features = ["energy*Instrumentalness", "acousticness^2", "valence^2", "loudness"]
    
    X_full = analysis_df[full_features]
    X_genre_artist = analysis_df[genre_artist_features]
    X_artist = analysis_df[artist_features]
    X_genre = analysis_df[genre_features]
    X_weak = analysis_df[weak_features]
    y = analysis_df['popularity']
    
    rand = 69
    
    models = {}
    
    X_train, _, y_train,_ = train_test_split(X_full, y, test_size=0.2, random_state=rand)
    models['full'] = LinearRegression().fit(X_train, y_train)
    
    X_train, _, y_train, _ = train_test_split(X_genre_artist, y, test_size=0.2, random_state=rand)
    models['genre_artist'] = LinearRegression().fit(X_train, y_train)
    
    X_train, _, y_train, _ = train_test_split(X_artist, y, test_size=0.2, random_state=rand)
    models['artist'] = LinearRegression().fit(X_train, y_train)
    
    X_train, _, y_train, _ = train_test_split(X_genre, y, test_size=0.2, random_state=rand)
    models['genre'] = LinearRegression().fit(X_train, y_train)
    
    X_train, _, y_train, _ = train_test_split(X_weak, y, test_size=0.2, random_state=rand)
    models['weak'] = LinearRegression().fit(X_train, y_train)
    
    return {
        'models': models,
        'genre_mean_dict': genre_mean_dict,
        'artist_mean_dict': artist_mean_dict,
        'median_artist': median_artist
    }

def predict_popularity(song_attrs, models_data):
    models = models_data['models']
    genre_mean_dict = models_data['genre_mean_dict']
    artist_mean_dict = models_data['artist_mean_dict']
    median_artist = models_data['median_artist']
    
    genre = song_attrs.get('track_genre','')
    genre_mean = genre_mean_dict.get(genre,np.nan)
    
    artists_str = song_attrs.get('artists', '')
    if pd.isna(artists_str) or artists_str == '':
        artist_mean = median_artist
        artist_known = False
    else:
        artist_list = [a.strip() for a in artists_str.split(';')]
        artist_means = [artist_mean_dict.get(a, np.nan) for a in artist_list]
        if any(pd.isna(m) for m in artist_means):
            artist_mean = median_artist
            artist_known = False
        else:
            artist_mean = np.mean(artist_means)
            artist_known = True
    

    genre_known = not pd.isna(genre_mean)
    

    energy_instrumentalness = song_attrs.get('instrumentalness', 0) *song_attrs.get('energy', 0)
    acousticness_sq = song_attrs.get('acousticness', 0)**2
    valence_sq = song_attrs.get('valence', 0)**2
    loudness = song_attrs.get('loudness', 0)
    

    if genre_known and artist_known:
        model = models['full']
        features = np.array([[artist_mean, energy_instrumentalness, acousticness_sq, 
                             valence_sq, genre_mean, loudness]])
    elif artist_known:
        model = models['artist']
        features = np.array([[artist_mean, energy_instrumentalness]])
    elif genre_known:
        model = models['genre']
        features = np.array([[genre_mean, energy_instrumentalness]])
    else:
        model = models['weak']
        features = np.array([[energy_instrumentalness, acousticness_sq, valence_sq, loudness]])
    
    prediction = model.predict(features)[0]
    prediction = max(0, min(100, prediction))
    return int(round(prediction))