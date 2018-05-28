from sqlalchemy import exc


class Access:
    def __init__(self, model, session):
        self.model = model
        self.session = session

    def get(self, record_id):
        try:
            record = self.model.query.filter_by(id=record_id).first()
            if not record:
                raise exc.SQLAlchemyError('Not Found')
            return record
        except exc.SQLAlchemyError:
            self.session.rollback()
            raise

    def list(self):
        try:
            return self.model.query.all()
        except exc.SQLAlchemyError:
            self.session.rollback()
            raise

    def search(self, name):
        try:
            return self.model.query.filter(
                self.model.name.ilike(name + '%')).all()
        except exc.SQLAlchemyError:
            self.session.rollback()
            raise

    def insert(self, **kwargs):
        try:
            record = self.model(**kwargs)
            self.session.add(record)
            self.session.commit()
            return record
        except exc.SQLAlchemyError:
            self.session.rollback()
            raise

    def get_or_insert(self, model, **kwargs):
        instance = self.session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = self.model(**kwargs)
            self.session.add(instance)
            self.session.commit()
            return instance

    def delete(self, record_id):
        try:
            record = self.model.query.filter_by(id=record_id).first()
            if not record:
                raise exc.SQLAlchemyError('Not Found')
            self.session.delete(record)
            self.session.commit()
            return record
        except exc.SQLAlchemyError:
            self.session.rollback()
            raise

    def __repr__(self):
        return '<Access>'
