from flask import Blueprint, jsonify, request
from ..models.database import query_db

rooms_blueprint = Blueprint('rooms', __name__, url_prefix='/api/rooms')

@rooms_blueprint.route('/', methods=['GET'])
def get_rooms():
    """
    GET /api/rooms

    Retrieve a list of all rooms with statistics

    RETURNS:
        List of rooms + message counts + user counts
    """

    rooms = query_db('''SELECT
                            r.*,
                            COUNT(DISTINCT p.serial) as msg_count,
                            COUNT(DISTINCT p.user_id) as unique_chatters
                        FROM room r
                        LEFT JOIN privmsg p ON r.room_id = p.room_id
                        GROUP BY r.room_id
                        ORDER BY msg_count DESC
                    ''')
    
    return jsonify({
        'data':rooms,
        'count':len(rooms)
    }), 200

@rooms_blueprint.route('/<room_id>', methods=['GET'])
def get_room(room_id):
    """
    GET /api/rooms/<room_id>

    Retrieve detailed information about a specific room

    RETURNS:
        room info with statistics
    """

    room = query_db(
        'SELECT * FROM room WHERE room_id = ?', (room_id,), one=True)
    
    if not room:
        return jsonify({
            'error': 'Not found',
            'message': f'Room {room_id} not found'
        }), 404
    
    msg_count = query_db(
        'SELECT COUNT(*) as count FROM privmsg WHERE room_id = ?', (room_id,), one=True)
    
    unique_chatters = query_db(
        'SELECT COUNT(DISTINCT user_id) as count FROM privmsg WHERE room_id = ?', (room_id,), one=True)
    
    top_chatters = query_db('''
                            SELECT
                                p.user_id,
                                u.display_name,
                                u.login,
                            COUNT(*) as msg_count
                            FROM privmsg p
                            LEFT JOIN user u ON p.user_id = u.user_id
                            WHERE p.room_id = ?
                            GROUP BY p.user_id
                            ORDER BY msg_count DESC
                            LIMIT 25
                            ''', (room_id,))
    
    sub_count = query_db(
        'SELECT COUNT(*) as count FROM sub WHERE room_id = ?', (room_id,), one=True)
     
    bits_total = query_db(
        'SELECT COALESCE(SUM(bits), 0) as total FROM bits WHERE room_id = ?', (room_id,), one=True)
    
    room_state = query_db(
        'SELECT * FROM roomstate WHERE room_id = ?', (room_id,), one=True)
    
    activity_by_hour = query_db('''
                                SELECT
                                    CAST(strftime('%H', timestamp) AS INTEGER) as hour,
                                    COUNT(*) as msg_count
                                FROM privmsg
                                WHERE room_id = ?
                                GROUP BY hour
                                ORDER BY hour
                                ''', (room_id,))
    
    return jsonify({
        'room': room,
        'stats': {
            'total_messages': msg_count['count'],
            'unique_chatters': unique_chatters['count'],
            'total_subscriptions': sub_count['count'],
            'total_bits': bits_total['total']

        },
        'top_chatters': top_chatters,
        'room_state': room_state,
        'activity_by_hour': activity_by_hour
    }), 200

@rooms_blueprint.route('/<room_id>/timeline', methods=['GET'])
def get_room_timeline(room_id):
    """
    GET /api/rooms/<room_id>/timeline

    Retrieve activity timeline for a room

    PARAMETERS:
        limit (int): Max events (dfault: 100)
        start_date (str): Filter from date
        end_date (str): Filter to date

    RETURNS:
        timeline for messages, subs, bits, raids
    """

    limit = min(request.args.get('limit', default=100, type=int), 1000)
    start_date = request.args.get('start_date', default=None, type=str)
    end_date = request.args.get('end_date', type=str)

    data_filter = ''
    params = [room_id]

    if start_date:
        date_filter += ' AND timestamp >= ?'
        params.append(start_date)
    if end_date:
        date_filter += ' AND timestamp <= ?'
        params.append(end_date)

    query = f'''
            SELECT
                'message' as event_type,
                timestamp,
                user_id,
                msg_content as content,
                serial as event_id
            FROM privmsg
            WHERE room_id = ? {date_filter}
            UNION ALL
            SELECT
            'subscription' as event_type,
            timestamp,
            user_id,
            system_msg as content,
            serial as event_id
            FROM sub
            WHERE room_id = ? {date_filter}
            UNION ALL
            SELECT
                'bits' as event_type,
                timestamp,
                user_id,
                'Cheered ' || bits || ' bits' as content,
                serial as event_id
            FROM bits
            WHERE room_id = ? {date_filter}
            UNION ALL
            SELECT
                'raid' as event_type,
                timestamp,
                user_id,
                system_msg as content,
                serial as event_id
            FROM raid
            WHERE room_id = ? {date_filter}
        )
        ORDER BY timestamp DESC
        LIMIT ?
    '''

    all_params = params * 4 + [limit]
    timeline = query_db(query, tuple(all_params))

    return jsonify({
        'room_id': room_id,
        'timeline': timeline,
        'count': len(timeline)
    }), 200
