class Song:
    def __init__(self, track_id, artists, album_name, track_name, popularity, duration_ms, explicit, danceability,
                 energy, key,loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo,
                 time_signature, track_genre):
        self.id = track_id
        self.artist = artists
        self.album = album_name
        self.name = track_name
        self.popularity = int(popularity)
        if popularity>100 or popularity<0:
            print("Error: wrong popularity")
            #raise ValueError("incorrect popularity")
        self.duration = duration_ms
        #explicit : has curse or not
        if explicit== "False":
            self.explicit = False
        elif explicit=="True":
            self.explicit = True
        else:
            print("Error: wrong explicity")
        if 0<danceability<1:
            self.danceabillity = danceability
        else:
            print("Error: wrong danceabillity")
            #raise ValueError("")
        if 0<energy<1:
            self.energy = energy
        else:
            print("Error: wrong energy")
        if 0<instrumentalness<1:
            self.instrumentalness = instrumentalness
        else:
            print("Error: wrong instrumentalness")
        if 0<acousticness<1:
            self.acousticness = acousticness
        else:
            print("Error: wrong acousticness")
        if 0<speechiness<1:
            self.speechiness = speechiness
        else:
            print("Error: wrong speechiness")
        #key: musical key 
        if 0<key<11:
            self.key = key
        else:
            print("Error: key was wrong")
        #mode: minor or major
        if mode==1 or mode==0:
            self.mode = mode
        else:
            print("Error: wrong mode entered")
        if 0<liveness<1:
            self.liveness = liveness
        else:
            print("Error: wrong liveness")
        if 0<valence<1:
            self.valence = valence
        else:
            print("Error: wrong valence")    
        self.genre = track_genre
        #loudness: 0 is most loud
        self.loudness = loudness
        #tempo : BPM
        self.tempo = tempo
        #time_signiture: usually 3,4,5 might be 0,1
        self.time_signiture = time_signature
        