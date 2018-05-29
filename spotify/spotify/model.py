from spotify.utils.models import get_or_create


class SpotifyLibrary:
    def __init__(self, tracks):
        self.songs = [t.__dict__ for t in tracks]

    # def to_list(self):
    #     return [t.__dict__ for t in self.songs]

    def normalize(self):
        result = {}

        artists = list(set([s['artist'] for s in self.songs]))

        for a in artists:
            result[a] = {'albums': {}}

        for song in self.songs:
            album = song['album']
            artist_albums = result[song['artist']]['albums']
            if album not in artist_albums:
                artist_albums[album] = {'songs': [song['name']]}
            else:
                artist_albums[album]['songs'].append(song['name'])

        return result

class SpotifyTrack:
    def __init__(self, track):
        self.added_at = track['added_at']
        self.name = track['track']['name']
        self.artist = track['track']['artists'][0]['name']
        self.album = track['track']['album']['name']