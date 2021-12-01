from swagger_server import db


class Blacklist(db.Model):

    __tablename__ = 'Blacklist'

    # A list of fields to be serialized
    SERIALIZE_LIST = ['id_user', 'id_blacklisted']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer)
    id_blacklisted = db.Column(db.Integer)

    def __init__(self, *args, **kw):
        super(Blacklist, self).__init__(*args, **kw)

    def serialize(self):
        return dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_LIST])
