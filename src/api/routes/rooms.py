from flask import Blueprint, jsonify, request
from ..models.database import query_db

room_blueprint = Blueprint('rooms', __name__, url_prefix='/api/rooms')

@room_blueprint.route('/', methods=['GET'])
def get_room():
    """
    GET /api/rooms
    """

    room_name = request.args.get('room-name', default=None, type=str)
    room_id = request.args.get('room-id', default=None, type=int)

    query = '''
            SELECT
                room_id,
                room_name
            FROM room
            WHERE 1=1
            '''

    params = []

    if room_name:
        query += ' AND room_name = ?'
        params.append(room_name)

    elif room_id:
        query += ' AND room_id = ?'
        params.append(room_id)

    room = query_db(query, tuple(params))

    if not room:
        return jsonify({
            'error': 'Not found',
            'message': f'Room {params[0]} not found.'
        }), 404
    
    return jsonify({
        'room_id': room['room_id'],
        'room_name': room['room_name']
    }), 200