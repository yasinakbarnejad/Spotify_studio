def get_genre_average(df):
    genre_average =  df.groupby('track_genre')['popularity'].agg(avg_popularity='mean').round(2).sort_values("avg_popularity", ascending=False).reset_index()
    return genre_average


def get_artist_average(df):
    df['artist'] = df['artists'].str.split(';')
    separated_df = df.explode('artist')
    separated_df['artist'] = separated_df['artist'].str.strip()
    artist_stat = separated_df.groupby("artist")["popularity"].agg(
        avg_popularity="mean", 
        hits = lambda x: (x>50).sum(),
        count = "count").sort_values("avg_popularity", ascending=False).reset_index()
    return artist_stat
    