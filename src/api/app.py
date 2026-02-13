from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config['JSON_SORT_KEYS'] = False
app.config['DATABASE'] = 'saltmine.db'

@app.route('/')
def home():
    """
    Root endpoint
    """
    return jsonify({
        'message': 'Saltmine API is running',
        'version': '1.0.1',
        'endpoints':{
            'messages': '/api/messages',
            'users': '/api/users',
            'health': '/api/health',
            'user stats': '/api/users/<user_id>',
            'user activity': '/api/users/<user_id>/activity'

        }
    })

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)