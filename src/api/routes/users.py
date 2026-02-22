from flask import Blueprint, jsonify, request
from ..models.database import query_db
from ..utils import utils

user_blueprint = Blueprint('users', __name__, url_prefix='/api/users')

@user_blueprint.route('/', methods=['GET'])
def get_users():
    """
    GET /api/users
    """
    room = request.args.get('room-name', default=None, type=str)

    limit = request.args.get('limit', default=500, type=int)
    offset = request.args.get('offset', default=0, type=int)

    limit = min(limit, 1000)    # upper limit per request

    try:
        query = '''
                SELECT
                    user_id,
                    display_name
                FROM user
                WHERE 1=1
                '''

        params = []

        if room is not None:
            query +=''' AND user_id IN (SELECT user_id 
                                        FROM privmsg 
                                        WHERE room_id = (SELECT room_id 
                                                         FROM room 
                                                         WHERE room_name = ?))'''
            params.append(room)

        query += ' ORDER BY display_name DESC' 
        query += ' LIMIT ? OFFSET ?'

        params.append(limit)
        params.append(offset)
        users = query_db(query, tuple(params))

        if users is None:
            return jsonify({
                'error': 'Not found',
                'message': 'No users found matching the criteria.'
            }), 404
        
        return jsonify({
            'users': users,
            'count': len(users),
            'limit': limit,
            'offset': offset,
            'hasMore': len(users) == limit
        }), 200

    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400
    
@user_blueprint.route('/single', methods=['GET'])
def get_user():
    """
    GET /api/users/single
    """
    try:
        username = request.args.get('user-name', default=None, type=str)
        user_id = request.args.get('user-id', default=None, type=int)

        query = '''
                SELECT
                    user_id,
                    display_name
                FROM user
                WHERE 1=1
                '''
        params = []

        if user_id is not None:
            query += ' AND user_id = ?'
            params.append(user_id)
        
        if username is not None:
            query += ' AND LOWER(display_name) = LOWER(?)'
            params.append(username)

        user = query_db(query, tuple(params), one=True)

        if user is None:
            return jsonify({
                'error': 'Not found',
                'message': 'No user found matching the criteria.'
            }), 404
        
        return jsonify({
            'user_id': user['user_id'],
            'display_name': user['display_name']
        }), 200

    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400
