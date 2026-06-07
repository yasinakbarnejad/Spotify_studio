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
        self.duration = int(duration_ms)
        #explicit : has curse or not
        self.explicit = explicit
        if 0<float(danceability)<1:
            self.danceabillity = float(danceability)
        else:
            print("Error: wrong danceabillity")
            #raise ValueError("")
        if 0<float(energy)<1:
            self.energy = float(energy)
        else:
            print("Error: wrong energy")
        if 0<float(instrumentalness)<1:
            self.instrumentalness = float(instrumentalness)
        else:
            print("Error: wrong instrumentalness")
            print("wrong", self.name)
        if 0<float(acousticness)<1:
            self.acousticness = float(acousticness)
        else:
            print("Error: wrong acousticness")
        if 0<float(speechiness)<1:
            self.speechiness = float(speechiness)
        else:
            print("Error: wrong speechiness")
        #key: musical key 
        if 0<=int(key)<=11:
            self.key = int(key)
        else:
            print("Error: key was wrong")
        #mode: minor or major
        mode = int(mode)
        if mode==1 or mode==0:
            self.mode = mode
        else:
            print("Error: wrong mode entered")
        liveness = float(liveness)
        if 0<liveness<1:
            self.liveness = liveness
        else:
            print("Error: wrong liveness")
        valence = float(valence)
        if 0<valence<1:
            self.valence = valence
        else:
            print("Error: wrong valence")    
        self.genre = track_genre
        #loudness: 0 is most loud
        self.loudness = float(loudness)
        #tempo : BPM
        self.tempo = float(tempo)
        #time_signiture: usually 3,4,5 might be 0,1
        self.time_signiture = int(time_signature)
    def to_dict(self):
        row = {
            "track_id": self.id, "artists": self.artist, "album_name":self.album, "track_name": self.name, 
            "popularity": self.popularity, "duration_ms": self.duration, "explicit":self.explicit, 
            "danceability":self.danceabillity,"energy":self.energy, "key":self.key,"loudness": self.loudness, 
            "mode": self.mode, "speechiness": self.speechiness, "acousticness":self.speechiness, 
            "instrumentalness":self.instrumentalness, "liveness":self.liveness, "valence":self.valence, 
            "tempo":self.tempo,"time_signature":self.time_signiture, "track_genre":self.genre
        }
        return row
        