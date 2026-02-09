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
    from .routes import privmsg
    app.register_blueprint(privmsg.msg_blueprint)

    # root endpoint

    @app.route('/')
    def home():
        return {
            'message':'Saltmine API',
            'version': '1.0.0',
            'endpoints': {
                'privmsg': '/api/privmsg',
                'privmsg_stats': '/api/privmsg/stats',
                'search': '/api/privmsg/search',
            }
        }
    
    return app