from flask import Flask
from flask_cors import CORS

from app.extensions import db
from app.config import Config


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:5173"
                ]
            }
        }
    )

    db.init_app(app)

    from app.blueprints.analysis import analysis_bp
    app.register_blueprint(analysis_bp)

    from app.blueprints.history import history_bp
    app.register_blueprint(history_bp)

    from app.blueprints.chat import chat_bp
    app.register_blueprint(chat_bp)

    from app.blueprints.users import users_bp
    app.register_blueprint(users_bp)

    from app.blueprints.weather import weather_bp
    app.register_blueprint(weather_bp)

    with app.app_context():
        db.create_all()

    return app