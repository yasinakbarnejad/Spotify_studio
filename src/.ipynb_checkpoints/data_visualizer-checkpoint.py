import matplotlib.pyplot as plt
import  src.data_analyzer
import numpy as np

def show_diffrence(before, after, variable):
    from seaborn import boxplot,stripplot
    boxplot(data=before[variable])
    stripplot(data=before[variable])
    plt.show()
    boxplot(data=after[variable])
    stripplot(data=after[variable])

    plt.show()
def plot_correlation_heatmap(df):
    from seaborn import heatmap
    int_df = df[["popularity", "danceability","energy","loudness","speechiness", "tempo", "acousticness"]].copy()
    corraltion = int_df.corr()
    heatmap(corraltion, annot=True,cmap='coolwarm',center=0,square=True,fmt='.2f',linewidths=0.5)
    plt.show()
def genres_chart(df):
    genre_average = src.data_analyzer.get_genre_average(df)
    sample = genre_average[0:30]
    fig, chart = plt.subplots()
    chart.bar(sample["track_genre"],sample["avg_popularity"])
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.tight_layout()
    plt.show()
def artist_chart(df):
    artist_average = src.data_analyzer.get_artist_average(df)
    sample = artist_average[artist_average["count"]>2]
    sample = sample[0:30]
    fig, chart = plt.subplots()
    chart.bar(sample["artist"],sample["avg_popularity"])
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.tight_layout()
    plt.show()
def dance_energy(df):
    import matplotlib.cm as cm
    genre_average = src.data_analyzer.get_genre_average(df)
    sample = genre_average['track_genre'][0:10].tolist()
    colors = cm.hsv(np.linspace(0, 1, 10))  
    fig, chart = plt.subplots()
    for genre, color in zip(sample, colors):
        mask = df['track_genre'] == genre
        chart.scatter(df[mask]["energy"][0:600],df[mask]["danceability"][0:600],s=8,color=color,label=genre)
    chart.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
     
    

#handler = data_cleaner.IQROutlierHandler()
#show_diffrence(df, handler.handle(df,"popularity"),"popularity")