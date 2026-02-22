from flask import Blueprint, jsonify, request
from ..models.database import query_db
from ..utils import utils

bits_blueprint = Blueprint('bits', __name__, url_prefix='/api/bits')

@bits_blueprint.route('/', methods=['GET'])
def get_bits():
    """
    GET /api/bits
    """

    try: 
        user_name = request.args.get('user-name', default=None, type=str)
        user_id = request.args.get('user-id', default=None, type=int)
        room_name = request.args.get('room-name', default=None, type=str)
        room_id = request.args.get('room-id', default=None, type=int)
        start_date = request.args.get('start-date', default=None, type=str)
        end_date = request.args.get('end-date', default=None, type=str)

        limit = request.args.get('limit', default=500, type=int)
        offset = request.args.get('offset', default=0, type=int)

        limit = min(limit, 1000)

        query = '''
                SELECT
                    b.timestamp,
                    b.bits,
                    u.display_name,
                    r.room_name
                FROM bits b
                LEFT JOIN room r ON b.room_id = r.room_id
                LEFT JOIN user u ON b.user_id = u.user_id
                WHERE 1=1
                '''
        params = []

        if user_name is not None:
            query += ' AND LOWER(b.display_name) = LOWER(?)'
            params.append(user_name)
        
        if user_id is not None:
            query += ' AND b.user_id = ?'
            params.append(user_id)

        if room_name is not None:
            query += ' AND LOWER(r.room_name) = LOWER(?)'
            params.append(room_name)

        if room_id is not None:
            query += ' AND b.room_id = ?'
            params.append(room_id)

        if start_date is not None:
            query += ' AND b.timestamp >= ?'
            params.append(utils.parse_date(start_date))

        if end_date is not None:
            query += ' AND b.timestamp <= ?'
            params.append(utils.parse_date(end_date, end_of_day=True))

        query += ' ORDER BY b.timestamp DESC'
        query += ' LIMIT ? OFFSET ?'

        params.extend([limit, offset])

        bits = query_db(query, tuple(params))

        if bits is None:
            return jsonify({
                'error': 'No entries were found matching the provided criteria.'
            }), 404
        
        return jsonify({
            'data': bits,
            'count': len(bits)
        }), 200

    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400