from flask import Flask, jsonify, request
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

    #####

    @app.route('/api/entries', methods=['GET'])
    def get_entries():
        entries = [
            {'type': 'info', 'text': 'Database connected', 'timestamp': '2024-06-01T12:00:00Z'},
            {'type': 'result', 'text': 'SELECT * FROM users returned 5 rows', 'timestamp': '2024-06-01T12:01:00Z'}
        ]
        return jsonify(entries), 200

    @app.route('/api/query', methods=['POST'])
    def execute_query():
        data=request.json
        query = data.get('query', '')
        try:
            # Mock response
            result = {
                'success': True,
                'rows': [{'id': 1, 'name': 'Example'}],
                'rowCount': 1
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    
    #####

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
            'message': 'The request was invalid or malformed',
            'status': 400
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
            'message': 'Something went wrong server-side'
        }), 500


    return app