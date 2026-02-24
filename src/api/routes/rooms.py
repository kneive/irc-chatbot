from flask import Blueprint, jsonify, request
from ..models.database import query_db

room_blueprint = Blueprint('rooms', __name__, url_prefix='/api/rooms')

@room_blueprint.route('/', methods=['GET'])
def get_rooms():
    """
    GET /api/rooms
    """

    try:

        room_name = request.args.get('room-name', default=None, type=str)
        room_id = request.args.get('room-id', default=None, type=int)

        limit = request.args.get('limit', default=500, type=int)
        offset = request.args.get('offset', default=0, type=int)

        limit = min(limit, 1000)

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

        query += ' ORDER BY room_name DESC'
        query += ' LIMIT ? OFFSET ?'

        params.extend([limit, offset])

        rooms = query_db(query, tuple(params))

        if not rooms:
            return jsonify({
                'data': [],
                'count': 0,
                'limit': limit,
                'offset': offset,
                'hasMore': False
            }), 200
        
        return jsonify({
            'data': rooms,
            'count': len(rooms),
            'limit': limit,
            'offset': offset,
            'hasMore': len(rooms) == limit
        }), 200
    
    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400
