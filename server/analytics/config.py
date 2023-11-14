import os

# secret key
SECRET_KEY = os.urandom(24)

# defines if app should run in dev or prod
FLASK_DEBUG = 1

# sqlalchemy DB path
SQLALCHEMY_DATABASE_URI = "sqlite:///analytics.db"
