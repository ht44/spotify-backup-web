from spotify.database import db


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'),
                          nullable=False)

    songs = db.relationship('Song', backref='album', lazy=True)

    @property
    def dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @property
    def songs_dict(self):
        return [song.dict for song in self.songs]

    def __repr__(self):
        return '<Album %r>' % self.name