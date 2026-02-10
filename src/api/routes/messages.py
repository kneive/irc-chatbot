from flask import Blueprint, jsonify, request
from ..models.database import query_db, execute_db

msg_blueprint = Blueprint('messages', __name__, url_prefix='/api/messages')

@msg_blueprint.route('/', methods=['GET'])
def get_privmsgs():
    """
    GET /api/messages

    Retrieve all messages or filter by query parameters

    QUERY PARAMETERS:
        limit: max number of messages to return
        offset: number of messages to skip
        user: filter by user
        channel: filter by channel

    RETURN:
        JSON object with 
            data: list of message objects
            count: number of messages returned
            total: total number of messages in database

    EXAMPLE:
        GET /api/privmsg
        GET /api/privmsg?limit=50
        GET /api/privmsg?user=random_user
        GET /api/privmsg?limit=50&offset=100
    """

    limit = request.args.get('limit', default=100, type=int)
    offset = request.args.get('offset', default=0, type=int)
    user_id = request.args.get('user_id', default=None, type=str)
    room_id = request.args.get('room_id', default=None, type=str)
    search = request.args.get('search', default=None, type=str)
    start_date = request.args.get('start_date', default=None, type=str)
    end_date = request.args.get('end_date', default=None, type=str)

    # building SQL query with optional filters
    query = '''
            SELECT p.*, u.display_name, u.login, r.room_name 
            FROM privmsg p
            LEFT JOIN user u ON p.user_id = u.user_id
            LEFT JOIN room r ON p.room_id = r.room_id
            '''
    
    conditions = []
    params = []

    # add WHERE conditions if filters are applied
    if user_id:
        conditions.append('p.user_id = ?')
        params.append(user_id)

    if room_id:
        conditions.append('p.room_id = ?')
        params.append(room_id)
    
    if search:
        conditions.append('p.msg_content LIKE ?')
        params.append(f'%{search}%')

    if start_date:
        conditions.append('p.timestamp >= ?')
        params.append(start_date)

    if end_date:
        conditions.append('p.timestamp <= ?')
        params.append(end_date)

    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    # add ordering and pagination
    query += ' ORDER BY timestamp DESC LIMIT ? OFFSET ?'
    params.extend([limit, offset])

    # execute query
    messages = query_db(query, tuple(params))

    # get total count
    count_query = 'SELECT COUNT(*) as count FROM privmsg'
    if conditions:
        count_query += ' WHERE ' + ' AND '.join(conditions)

    total = query_db(count_query, tuple(params[:-2]), one=True)['count']

    return jsonify({
        'data': messages,
        'count': len(messages),
        'total': total,
        'limit': limit,
        'offset': offset,
        'filters': {
            'room_id': room_id,
            'user_id': user_id,
            'search': search,
            'start_date': start_date,
            'end_date': end_date
        }
    }), 200

@msg_blueprint.route('/<int:serial>', methods=['GET'])
def get_message(serial):
    """
    GET /api/messages/<serial>
    
    Retrieve a single message by ID

    PARAMETERS
        serial

    RETURN
        JSON object with message data or 404

    EXAMPLE
        GET /api/messages/42
    """

    message = query_db('''
                       SELECT p.*, u.display_name, u.login,r.room_name 
                       FROM privmsg p
                       LEFT JOIN user u ON p.user_id = u.user_id
                       LEFT JOIN room r ON p.room_id = r. room_id
                       WHERE p.serial = ?
                       ''',(serial,), one=True)

    if message is None:
        return jsonify({
            'error': 'Not found',
            'message': f'Message with ID {serial} does not exist'
        }), 404
    
    return jsonify({'data': message}), 200

@msg_blueprint.route('/stats', methods=['GET'])
def get_message_stats():
    """
    GET /api/messages/stats

    Retrieve statistics about messages

    RETURNS
        JSON object with
            "total_messages": total number of messages,
            "unique_users": number of unique users,
            "unique_rooms": number of unique rooms,
            "date_range": {
                "earliest": i.e. "2023-01-01 00:00:00",
                "latest": i.e. "2023-12-31 23:59:59"
            },
            "messages_by_room": number of messages per room
            "top_users": users with 50 most messages
            "message_by_hour":
            "messages_by_day_of_week":
    """

    room_id = request.args.get('room_id', Default=None, type=str)
    user_id = request.args.get('user_id', Default=None, type=str)

    conditions = ''
    params = []

    if room_id:
        conditions = 'WHERE room_id = ?'
        params.append(room_id)
    elif user_id:
        conditions = 'WHERE user_id = ?'
        params.append(user_id)

    total = query_db(
        f'SELECT COUNT(*) as count FROM privmsg {conditions}',
        tuple(params), 
        one=True
    )

    unique_users = query_db(
        f'SELECT COUNT(DISTINCT user_id) AS count FROM privmsg {conditions}',
        tuple(params), 
        one=True
    )

    unique_rooms = query_db(
        f'SELECT COUNT(DISTINCT room_id) as count FROM privmsg {conditions}',
        tuple(params),
        one=True
    )

    date_range = query_db(
        f'''SELECT
                MIN(timestamp) as earliest,
                MAX(timestamp) as latest
            FROM privmsg {conditions}
        ''', tuple(params), one=True
    )

    messages_by_room = query_db(f'''
        SELECT
            p.room_id,
            r.room_name,
            COUNT(*) as message_count
        FROM privmsg p
        LEFT JOIN room r ON p.room_id = r.room_id
        {conditions}
        GROUP BY p.room_id
        ORDER BY message_count DESC
        LIMIT 30
    ''', tuple(params))
    
    top_chatters = query_db(f'''
        SELECT 
            p.user_id, 
            u.display_name,
            u.login,    
            COUNT(*) as msg_count
        FROM privmsg p
        LEFT JOIN user u ON p.user_id = u.user_id
        {conditions}
        GROUP BY p.user_id
        ORDER BY msg_count DESC
        LIMIT 50     
    ''', tuple(params))

    messages_by_hour = query_db(f'''
        SELECT
            CAST(strftime('%H', timestamp) AS INTEGER) as hour,
            COUNT(*) as msg_count
        FROM privmsg
        {conditions}
        GROUP BY hour
        ORDER BY hour
    ''', tuple(params))

    messages_by_day = query_db(f'''
        SELECT
            CAST(strftime('%w', timestamp) AS INTEGER) as day_of_week,
            COUNT(*) as msg_count
        FROM privmsg
        {conditions}
        GROUP BY day_of_week
        ORDER BY day_of_week
    ''', tuple(params))

    return jsonify({
        'total_messages': total['count'],
        'unique_users': unique_users['count'],
        'unique_rooms': unique_rooms['count'],
        'date_range': date_range,
        'messages_by_room': messages_by_room,
        'top_chatters': top_chatters,
        'messages_by_hour': messages_by_hour,
        'messages_by_day_of_week': messages_by_day
    }), 200

@msg_blueprint.route('/thread/<message_id>', methods=['GET'])
def get_message_thread(message_id):
    """
    GET /api/messages/thread/<message_id>

    Retrieve a message and its replies (thread view)

    PARAMETERS
        message_id: message_id to get thread for

    RETURNS
        JSON object with
            "original_message":
            "replies"
    """

    original = query_db('''
        SELECT
            p.*,
            u.display_name,
            u.login,
            r.room_name
        FROM privmsg p
        LEFT JOIN user u ON p.user_id = u.user_id
        LEFT JOIN room r ON p.room_id = r.room_id
        WHERE p.message_id = ?
    ''', (message_id,), one=True)

    if not original:
        return jsonify({
            'error': 'Not found',
            'message': f'Message with ID {message_id} not found'
        }), 404

    replies = query_db('''
        SELECT
            p.*,
            u.display_name,
            u.login,
            r.room_name
        FROM privmsg p
        LEFT JOIN user u ON p.user_id = u.user_id
        LEFT JOIN room r ON p.room_id = r.room_id
        WHERE p.reply_msg_id = ?
        ORDER BY p.timestamp ASC
    ''', (message_id,))

    return jsonify({
        'original_message': original,
        'replies': replies,
        'reply_count': len(replies)
    }), 200

@msg_blueprint.route('/search', methods=['GET'])
def search_privmsgs():
    """
    GET /api/messages/search

    Search privmsgs by content

    PARAMETERS
        query: search query (required)
        limit: max number of results (default 50)

    RETURNS
        JSON object with matching messages

    EXAMPLE
        GET /api/privmsg/search?query=hello&limit=100
    """

    search_query = request.args.get('query', type=str)
    limit = request.args.get('limit', default=50, type=int)

    if not search_query:
        return jsonify({
            'error': 'Bad request',
            'message': 'Search query parameter "query" is required'
        }), 400
    
    results = query_db('''
                SELECT * FROM privmsg
                WHERE msg_content LIKE ?
                ORDER BY timestamp DESC
                LIMIT ?        
            ''', (f'%{search_query}%', limit))
    
    return jsonify({
        'data': results,
        'count': len(results),
        'query': search_query
    }), 200