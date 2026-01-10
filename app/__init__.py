import os
from flask import Flask
from dotenv import load_dotenv

from .extensions import db, migrate

def create_app():
    load_dotenv()  # loads .env (read it)

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///library.db") #fallback
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import api
    app.register_blueprint(api) #blueprint to collect the routes in one place

    return app
