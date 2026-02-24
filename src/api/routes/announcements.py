from flask import Blueprint, jsonify, request
from ..models.database import query_db
from ..utils import utils

announcement_blueprint = Blueprint('announcements', __name__, url_prefix='/api/announcements')

@announcement_blueprint.route('/', methods=['GET'])
def get_announcements():
    """
    GET /api/announcements
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
                    r.room_name,
                    a.display_name,
                    a.msg_content,
                    a.timestamp
                FROM announcement a
                JOIN room r ON a.room_id = r.room_id
                WHERE 1=1
                '''
        
        params = []

        if user_name is not None:
            query += ' AND a.display_name = ?'
            params.append(user_name)

        if user_id is not None:
            query += ' AND a.user_id = ?'
            params.append(user_id)

        if room_name is not None:
            query += ' AND r.room_name = ?'
            params.append(room_name)

        if room_id is not None:
            query += ' AND r.room_id = ?'
            params.append(room_id)

        if start_date is not None:
            query += ' AND a.timestamp >= ?'
            params.append(utils.parse_date(start_date))

        if end_date is not None:
            query += ' AND a.timestamp <= ?'
            params.append(utils.parse_date(end_date, end_of_day=True))

        query += ' ORDER BY a.timestamp DESC'
        query += ' LIMIT ? OFFSET ?'

        params.extend([limit, offset])    

        announcements = query_db(query, params)

        if announcements is None:
            return jsonify({
                'data': [],
                'count': 0,
                'limit': limit,
                'offset': offset,
                'hasMore': False
            }), 200
        
        return jsonify({
            'data': announcements,
            'count': len(announcements),
            'limit': limit,
            'offset': offset,
            'hasMore': len(announcements) == limit
        }), 200

    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400