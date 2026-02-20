from flask import Blueprint, jsonify, request
from ..models.database import query_db
from ..utils import utils

msg_blueprint = Blueprint('messages', __name__, url_prefix='/api/messages')

@msg_blueprint.route('/', methods=['GET'])
def get_messages():
    """
    GET /api/messages
    """

    user_name = request.args.get('user-name', default=None, type=str)
    user_id = request.args.get('user-id', default=None, type=int)
    room_name = request.args.get('room-name', default=None, type=str)
    room_id = request.args.get('room-id', default=None, type=int)
    start_date = request.args.get('start-date', default=None, type=str)
    end_date = request.args.get('end-date', default=None, type=str)
    #all = request.args.get('all', default=False, type=bool)
    
    try:
        query = '''
                SELECT
                    u.display_name,
                    r.room_name,
                    m.msg_content,
                    m.reply_msg_body,
                    m.timestamp
                FROM privmsg m
                JOIN user u ON m.user_id = u.user_id
                JOIN room r ON m.room_id = r.room_id
                WHERE 1=1
                '''

        params = []

        if user_name is not None:
            query += ' AND u.display_name = ?'
            params.append(user_name)

        if user_id is not None:
            query += ' AND u.user_id = ?'
            params.append(user_id)

        if room_name is not None:
            query += ' AND r.room_name = ?'
            params.append(room_name)

        if room_id is not None:
            query += ' AND r.room_id = ?'
            params.append(room_id)

        if start_date is not None:
            parsed_date = utils.parse_date(start_date)
            query += ' AND m.timestamp >= ?'
            params.append(parsed_date)        

        if end_date is not None:
            parsed_date = utils.parse_date(end_date, end_of_day=True)
            query += ' AND m.timestamp <= ?'
            params.append(parsed_date)

        query += ' ORDER BY m.timestamp DESC'

        messages = query_db(query, tuple(params))

        if messages is None:
            return jsonify({
                'error': 'Not found',
                'message': 'No messages found matching the criteria.'
            }), 404

        return jsonify({
            'messages': messages,
            'count': len(messages)
        }), 200

    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400