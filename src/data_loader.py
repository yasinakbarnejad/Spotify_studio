import pandas as pd
from tqdm import tqdm
from src.song import Song
import os
import csv

#for better intution in loading and memory reason 
CSV_CHUNK_SIZE = 1000

def load_file(file_path="data/dataset.csv"):
    chunks = []
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: Wrong file name.Wanna use default dataset?")
        
    for chunk in tqdm(pd.read_csv(file_path, chunksize=CSV_CHUNK_SIZE),desc="Loading dataset", unit="song_packs"):
        chunks.append(chunk)
    table = pd.concat(chunks,ignore_index=True)
    return table
def classify_data(df):
    songs = []
    bad_song = []
    for idx,row in tqdm(df.iterrows(),desc="classifying songs",unit="songs"):
        try:
            song = Song(row["track_id"],row["artists"],row["album_name"],row["track_name"],row["popularity"],row["duration_ms"],
                        row["explicit"],row["danceability"],row["energy"],row["key"],row["loudness"],row["mode"],
                        row["speechiness"],row["acousticness"],row["instrumentalness"],row["liveness"],row["valence"],
                        row["tempo"],row["time_signature"],row["track_genre"])
            songs.append(song)
        except ValueError:
            bad_song.append(idx)
    print(f"Removed {len(bad_song)} invalid songs")
    df.drop(index=bad_song, inplace=True)
    return df
def append_song(song:Song, df):
    song_dict = song.to_dict()    
    with open("data/dataset.csv", 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
    with open("data/dataset.csv", 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writerow(song_dict)
    df.loc[len(df)] = song_dict