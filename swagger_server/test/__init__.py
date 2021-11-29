import logging

import connexion
from flask_testing import TestCase

from swagger_server.encoder import JSONEncoder


class BaseTestCase(TestCase):

    def create_app(self):
        from swagger_server import create_app, db
        app = create_app()
        print("test db ", db)
        return app
