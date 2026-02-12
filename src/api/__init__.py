from flask import Flask
from flask_cors import CORS
from .models import database
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'saltmine.db'

def create_app(config=None):
    """
    App factory
    """

    app = Flask(__name__)

    app.config.from_mapping(
        DATABASE=DB_PATH,
        JSON_SORT_KEYS=False,
    )

    # applies custom config if provided
    if config:
        app.config.update(config)

    CORS(app)

    # init database
    database.init_app(app)

    # register blueprints
    from .routes import messages, users, rooms, stats
    app.register_blueprint(messages.msg_blueprint)
    app.register_blueprint(users.users_blueprint)
    app.register_blueprint(rooms.rooms_blueprint)
    app.register_blueprint(stats.stats_bluepint)

    # root endpoint

    @app.route('/')
    def home():
        return {
            'message':'Saltmine API',
            'version': '1.0.1',
            'endpoints': {
                'messages': '/api/messages',
                'message stats': '/api/messages/stats',
                'search': '/api/messages/search',
                'users': '/api/users',
                'user stats': '/api/users/<user_id>',
                'user activity': '/api/users/<user_id>/activity'
            }
        }
    
    return app