from spotify.utils.access import Access


class ArtistAccess(Access):
    def __init__(self, model, session):
        super(ArtistAccess, self).__init__(model, session)

    def __repr__(self):
        return '<Access Artist>'
