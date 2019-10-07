from config import Config

from flask import Flask

from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from app.chats import bp as chats
    app.register_blueprint(chats, url_prefix='/chats')

    from app.messages import bp as messages
    app.register_blueprint(messages, url_prefix='/messages')

    from app.users import bp as users
    app.register_blueprint(users, url_prefix='/users')

    from app.errors import bp as errors
    app.register_blueprint(errors)

    from app.errors.errors import bad_request, not_found_error, internal_server_error
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_server_error)


    return app


from app import models
