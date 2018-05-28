from spotify.utils.access import Access


class AlbumAccess(Access):
    def __init__(self, model, session):
        super(AlbumAccess, self).__init__(model, session)

    def __repr__(self):
        return '<Access Album>'
