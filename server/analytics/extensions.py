from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

# Sqlalchemy instance
db = SQLAlchemy()

# flask migrate
migrate = Migrate()

# flask restful
api = Api()
