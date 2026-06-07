import pandas as pd
import time
from tqdm import tqdm
from song import Song
import os

chunk_size = 1000

def load_file(file_path="data/dataset.csv"):
    chunks = []
    if not os.path.exists(file_path):
        print("Error: Wrong file name.Wanna use defualt dataset?")
    for chunk in tqdm(pd.read_csv(file_path, chunksize=chunk_size),desc="Loading dataset", unit="song_packs"):
        chunks.append(chunk)
    table = pd.concat(chunks,ignore_index=True)
    return table
def classify_data(df):
    songs = []
    for _,row in tqdm(df.iterrows(),desc="calssifing songs",unit="songs"):
        song = Song(row["track_id"],row["artists"],row["album_name"],row["track_name"],row["popularity"],row["duration_ms"],
                    row["explicit"],row["danceability"],row["energy"],row["key"],row["loudness"],row["mode"],
                    row["speechiness"],row["acousticness"],row["instrumentalness"],row["liveness"],row["valence"],
                    row["tempo"],row["time_signature"],row["track_genre"])
        songs.append(song)
        
df = load_file()
classify_data(df)