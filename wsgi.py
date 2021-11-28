"""
Message in a Bottle
Web Server Gateway Interface

This file is the entry point for
mib-users-ms microservice.
"""
from swagger_server import create_app

# application instance
app = create_app()

if __name__ == '__main__':
    app.run()
