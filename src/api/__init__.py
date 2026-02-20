from .routes.old_routes import messages, rooms
from flask import Flask, jsonify, request
from flask_cors import CORS
from .models import database
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent/ 'database' / 'saltmine.db'

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
    from .routes import announcements, gifts, messages, rooms, subs
    app.register_blueprint(announcements.announcement_blueprint)
    app.register_blueprint(gifts.gift_blueprint)
    app.register_blueprint(messages.msg_blueprint)
    app.register_blueprint(rooms.room_blueprint)
    app.register_blueprint(subs.sub_blueprint)

    # root endpoint

    @app.route('/')
    def home():
        return {
            'message':'Saltmine API',
            'version': '1.0.0',
            'endpoints': {
            }
        }

    @app.route('/api/health')
    def health():
        """
        Health check endpoint
        """

        return jsonify({'status': 'ok'}), 200

    @app.errorhandler(400)
    def bad_request(error):
        """
        Handles 400 errors
        """
        return jsonify({
            'error': 'Bad request',
            'message': 'The request is invalid or malformed',
        }), 400


    @app.errorhandler(404)
    def not_found(error):
        """
        Handles 404 errors
        """
        return jsonify({
            'error': 'Not found',
            'message': 'The requested resource does not exist'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        """
        Handles 500 (server) errors 
        """

        return jsonify({
            'error': 'Internal server error',
            'message': 'Something went wrong'
        }), 500


    return app