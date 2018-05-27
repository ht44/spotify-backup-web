class SpotifyLibrary:
    def __init__(self, tracks):
        self.tracks = tracks

    def to_list(self):
        return [t.__dict__ for t in self.tracks]


class SpotifyTrack:
    def __init__(self, track):
        self.added_at = track['added_at']
        self.name = track['track']['name']
        self.artist = track['track']['artists'][0]['name']
        self.album = track['track']['album']['name']

    def print_hi(self):
        print('hello')