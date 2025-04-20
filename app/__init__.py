from flask import Flask
from app.models import db
from app.errors import register_error_handlers  # Make sure this exists
import logging
from logging.handlers import RotatingFileHandler
import os
from flasgger import Swagger


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)

    # Register blueprints
    from app.routes import bp
    app.register_blueprint(bp)

    # ✅ Register error handlers after app is created
    register_error_handlers(app)

    
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=3)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('App startup')

    Swagger(app)  # ✅ Register Swagger here
    return app
