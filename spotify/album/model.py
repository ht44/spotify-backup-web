from spotify.database import db


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'),
                          nullable=False)

    songs = db.relationship('Song', backref='songs', lazy=True)
    artist = db.relationship('Artist', backref='artist', lazy=True, uselist=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'artist_id': self.artist_id,
            'artist': self.artist.name,
            'songs': self.serialize_songs
        }

    @property
    def serialize_songs(self):
        return [songs.serialize for songs in self.songs]

    def __repr__(self):
        return '<Album %r>' % self.name