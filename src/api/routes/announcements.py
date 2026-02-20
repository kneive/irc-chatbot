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
            parsed_date = utils.parse_date(start_date)
            query += ' AND a.timestamp >= ?'
            params.append(parsed_date)

        if end_date is not None:
            parsed_date = utils.parse_date(end_date, end_of_day=True)
            query += ' AND a.timestamp <= ?'
            params.append(parsed_date)

        announcements = query_db(query, params)

        if announcements is None:
            return jsonify({
                'error': 'Not found',
                'message': 'No announcements found matching the criteria.'
            }), 404
        
        return jsonify({
            'announcements': announcements,
            'count': len(announcements)
        }), 200

    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400