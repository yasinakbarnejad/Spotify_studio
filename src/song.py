from  dataclasses import dataclass, asdict
SONG_FIELDS = [
            {"key": "track_id",   "label": "Track ID",        "type": str},
            {"key": "artists",    "label": "Artists",         "type": str},
            {"key": "album_name", "label": "Album Name",      "type": str},
            {"key": "track_name", "label": "Track Name",      "type": str},
            {"key": "duration_ms","label": "Duration (ms)",   "type": int},
            {"key": "explicit",   "label": "Explicit", "type": bool},
            {"key": "danceability","label": "Danceability",   "type": float, "min": 0.0, "max": 1.0},
            {"key": "energy",     "label": "Energy",          "type": float, "min": 0.0, "max": 1.0},
            {"key": "key",        "label": "Key",      "type": int, "min": 0, "max": 11},
            {"key": "loudness",   "label": "Loudness",        "type": float},
            {"key": "mode",       "label": "Mode",      "type": int, "min": 0, "max": 1},
            {"key": "speechiness","label": "Speechiness",     "type": float, "min": 0.0, "max": 1.0},
            {"key": "acousticness","label": "Acousticness",   "type": float, "min": 0.0, "max": 1.0},
            {"key": "instrumentalness","label": "Instrumentalness", "type": float, "min": 0.0, "max": 1.0},
            {"key": "liveness",   "label": "Liveness",        "type": float, "min": 0.0, "max": 1.0},
            {"key": "valence",    "label": "Valence",         "type": float, "min": 0.0, "max": 1.0},
            {"key": "tempo",      "label": "Tempo",     "type": float},
            {"key": "time_signature","label": "Time Signature", "type": int},
            {"key": "track_genre","label": "Track Genre",     "type": str},
            {"key": "popularity", "label": "Popularity",      "type": int, "min": 0, "max": 100}
        ]

@dataclass
class Song:
    track_id: str
    artists: str
    album_name: str
    track_name: str
    popularity: int
    duration_ms: int
    explicit: bool
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    time_signature: int
    track_genre: str
    def __post_init__(self):
        for field in SONG_FIELDS:
            key = field["key"]
            expeceted_type = field["type"]
            info = getattr(self, key)
            if not isinstance(info, expeceted_type):
                raise ValueError(f"{field["label"]} Must be {expeceted_type}")
            if "min" in field and not (field["min"] <= info <= field["max"]):
                raise ValueError(f"{field["label"]} Must be between {field['min']} and {field['max']}")                    
    def to_dict(self):
        return asdict(self)
    @classmethod
    def new_song(cls):
        data = cls.collect_data()
        return Song(**data)
    @staticmethod
    def collect_data():
        data = {}
        print("\n---Enter Song Details---")
        for field in SONG_FIELDS:
            while True:
                if field["key"]=="popularity":
                    choice = input("If you want to use ML enter yes, else enter the popularity yourself")
                    if choice == "yes":
                        pass #use ML to predict popularity
                    else: 
                        info = choice
                else:
                    info = input(f"{field['label']}: ")
                try:
                    if field["type"] == bool:
                        value = info.lower()== "true"
                    else:
                        value = field["type"](info)
                    
                    if "min" in field and not (field["min"] <= value <= field["max"]):
                        raise ValueError(f"{field["label"]} Must be between {field['min']} and {field['max']}")
                    
                    data[field["key"]] = value
                    break
                    
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}. Please try again.")
        return data            