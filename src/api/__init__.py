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
        JSONIFY_PRETTYPRINT_REGULAR=True
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
    app.register_blueprint(stats.stats_blueprint)

    # root endpoint

    @app.route('/')
    def home():
        return {
            'message':'Saltmine API',
            'version': '1.0.0',
            'endpoints': {
                'messages': { 
                    'list':'GET /api/messages',
                    'get_one': 'GET /api/messages/<serial>',
                    'statistics': 'GET /api/messages/stats',
                    'thread': 'GET /api/messages/thread/<msg_id>',
                    'search': 'GET /api/messages/search?query='
                },
                'users': {
                    'list': 'GET /api/users',
                    'get_one': 'GET /api/users/<user_id>',
                    'activity': 'GET /api/users/<user_id>/activity'
                },
                'rooms': {
                    'list': 'GET /api/rooms',
                    'get_one': 'GET /api/rooms/<room_id>',
                    'timeline': 'GET /api/rooms/<room_id>/timeline'
                },
                'stats': {
                    'overview': 'GET /api/stats/overview',
                    'subscriptions': 'GET /api/stats/subscriptions',
                    'bits': 'GET /api/stats/bits',
                    'raids': 'GET /api/stats/raids'
                }
            }
        }
    
    return app