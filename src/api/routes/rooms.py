from flask import Blueprint, jsonify, request
from ..models.database import query_db

room_blueprint = Blueprint('rooms', __name__, url_prefix='/api/rooms')

@room_blueprint.route('/name', methods=['GET'])
def get_room_by_name(room_name):
    """
    GET /api/rooms
    """

    room = query_db(
        'SELECT room_name, room_id FROM room WHERE name = ?', (room_name,), one=True
        )
    
    if not room:
        return jsonify({
            'error': 'Not found',
            'message': f'Room {room_name} not found'
        }), 404
    
    return jsonify({
        'id': room['room_id'],
        'name': room['room_name']
    }), 200

@room_blueprint.route('/<int:room_id>', methods=['GET'])
def get_room_by_id(room_id):
    """
    GET /api/rooms/<room_id>
    """

    room = query_db(
        'SELECT room_name, room_id FROM room WHERE room_id = ?', (room_id,), one=True
    )

    if not room:
        return jsonify({
            'error': 'Not found',
            'message': f'Room with ID {room_id} not found'
        }), 404
    
    return jsonify({
        'id': room['room_id'],
        'name': room['room_name']
    }), 200