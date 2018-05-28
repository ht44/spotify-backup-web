from spotify.database import db


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False, nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'),
                         nullable=False)

    # album = db.relationship('Album', backref='album', lazy=True, uselist=False)

    @property
    def dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return '<Song %r>' % self.name