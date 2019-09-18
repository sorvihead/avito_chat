from config import Config
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.chats import bp as chats
    app.register_blueprint(chats, url_prefix='/chats')

    from app.messages import bp as messages
    app.register_blueprint(messages, url_prefix='/messages')

    from app.users import bp as users
    app.register_blueprint(users, url_prefix='/users')

    return app

from app import models