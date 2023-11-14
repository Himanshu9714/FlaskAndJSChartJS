from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from .extensions import db
from .extensions import migrate
from .extensions import api


def create_app():
    """Create flask app."""

    # Flask app instance
    app = Flask(__name__)

    # Allow all origins
    CORS(app)

    # configure app
    configure_app(app)

    # configure extensions for app
    configure_extensions(app)

    # configure flask cli
    configure_app_cli(app)

    return app


def configure_app(app: Flask):
    """configure app."""

    # app configuration loaded from config file
    app.config.from_pyfile("config.py")


def configure_extensions(app: Flask):
    """Configure app extensions"""

    # Load all the DB models
    from .models import Sector
    from .models import Source
    from .models import Region
    from .models import Country
    from .models import Topic
    from .models import Analytics

    # Initialize the sqlalchemy with app
    db.init_app(app)

    # Intialize flask migrate
    migrate.init_app(app=app, db=db)

    # Configure the API routers
    from .routers.analytics import AnalyticsView
    from .routers.analytics import IntensityRelevanceLikelihoodChartView
    from .routers.analytics import NoOfRecordsByGroupView
    from .routers.analytics import GetYearsView

    # API endpoints
    api.add_resource(AnalyticsView, "/get-rows")
    api.add_resource(IntensityRelevanceLikelihoodChartView, "/get-stats")
    api.add_resource(NoOfRecordsByGroupView, "/get-counts")
    api.add_resource(GetYearsView, "/get-years-values")
    api.init_app(app)


def configure_app_cli(app: Flask):
    """Configure app cli."""
    from .scripts.load_data import cli

    # Add the flask cli
    app.cli.add_command(cli)
