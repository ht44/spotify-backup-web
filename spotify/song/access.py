from spotify.utils.access import Access


class SongAccess(Access):
    def __init__(self, model, session):
        super(SongAccess, self).__init__(model, session)

    def __repr__(self):
        return '<Access Song>'
