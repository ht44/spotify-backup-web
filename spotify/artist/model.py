from spotify.database import db


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    albums = db.relationship('Album', backref='artist', lazy=True)

    @property
    def dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @property
    def serialize_albums(self):
        return [album.serialize for album in self.albums]

    @property
    def albums_dict(self):
        return [album.dict for album in self.albums]

    @property
    def songs_dict(self):
        return [song.dict for album in self.albums for song in album.songs]

    def get_songs(self):
        return [song for album in self.albums for song in album.songs]

    def __repr__(self):
        return '<Artist %r>' % self.name
