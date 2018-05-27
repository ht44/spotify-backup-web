from spotify.database import db


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    albums = db.relationship('Album', backref='albums', lazy=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'albums': self.serialize_albums
        }

    @property
    def serialize_albums(self):
        return [album.serialize for album in self.albums]

    def __repr__(self):
        return '<Artist %r>' % self.name
