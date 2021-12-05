#!/bin/bash

# set the env to development
export FLASK_DEBUG=true
export FLASK_ENV=development

flask db init
flask db migrate
flask run
