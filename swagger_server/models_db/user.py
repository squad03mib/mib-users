from werkzeug.security import generate_password_hash, check_password_hash

from swagger_server import db


class User(db.Model):
    """Representation of User model."""

    # The name of the table that we explicitly set
    __tablename__ = 'User'

    # A list of fields to be serialized
    SERIALIZE_LIST = ['id', 'email', 'is_active',
                      'authenticated', 'is_anonymous', 'firstname',
                      'lastname', 'date_of_birth','is_reported']

    # All fields of user
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False)
    firstname = db.Column(db.Unicode(128), nullable=False, unique=False)
    lastname = db.Column(db.Unicode(128), nullable=False, unique=False)
    password = db.Column(db.Unicode(128))
    date_of_birth = db.Column(db.Date())
    is_active = db.Column(db.Boolean, default=True)
    is_reported = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    authenticated = db.Column(db.Boolean, default=True)
    is_anonymous = False

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self.authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def set_email(self, email):
        self.email = email

    def set_first_name(self, name):
        self.firstname = name

    def set_last_name(self, name):
        self.lastname = name

    def set_date_of_birth(self, date):
        self.date_of_birth = date

    def set_is_reported(self):
        self.is_reported = True

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self.authenticated = checked
        return self.is_active and self.authenticated

    def serialize(self):
        return dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_LIST])
