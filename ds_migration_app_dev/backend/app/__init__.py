from flask import Flask
from flask_cqlalchemy import CQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)

if app.config["ENV"] == "development":
    # Using a development configuration
    app.config.from_object('backend.config.config.DevelopmentConfig')
else:
    # Using a production configuration
    app.config.from_object('backend.config.config.ProductionConfig')

# db = CQLAlchemy(app)
# migrate = Migrate(app, db)

from backend.app.routes import routes, project, file_upload, collections
