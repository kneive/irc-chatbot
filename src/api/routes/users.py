from flask import Blueprint, jsonify, request
from ..models.database import query_db

users_blueprint = Blueprint('users', __name__, url_prefix='/api/users')

@users_blueprint.route('/', methods=['GET'])
def get_users():
    """
    GET /api/users

    Retrieve a list of user with optional filtering

    PARAMETERS:
        limit (int): max users to return
        offset (int): pagination offset
        search (str): search in login or display_name
        turbo (bool): filte by turbo

    RETURNS:
        List of user objects with message counts
    """

    limit = min(request.args.get('limit', default=100, type=int), 1000)
    offset = request.args.get('offset', default=0, type=int)
    search = request.args.get('search', default=None, type=str)
    turbo = request.args.get('turbo', default=None, type=int)

    query = '''
            SELECT
                u.*,
                COUNT(DISTINCT p.serial) as msg_count
            FROM user u
            LEFT JOIN privmsg p ON u.user_id = p.user_id
            '''
    
    conditions = []
    params = []

    if search:
        conditions.append('(u.login LIKE ? OR u.display_name LIKE ?)')
        params.extend([f'%{search}%', f'%{search}%'])

    if turbo is not None:
        conditions.append('u.turbo = ?')
        params.append(turbo)

    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    query += ' GROUP BY u.user_id ORDER BY msg_count DESC LIMIT ? OFFSET ?'
    params.extend([limit, offset])

    users = query_db(query, tuple(params))

    count_query = 'SELECT COUNT(*) as count FROM  user u'
    if conditions:
        count_query += ' WHERE ' + ' AND '.join(conditions)
    total = query_db(count_query, tuple(params[:-2]) if params[:-2] else (), one=True)['count']

    return jsonify({
        'data': users,
        'count': len(users),
        'total': total,
        'limit': limit,
        'offset': offset
    }), 200

#####

@users_blueprint.route('/all', methods=['GET'])
def get_all_users():
    """
    Get /api/users/all

    Get a list of all known users
    """

    users = query_db('SELECT display_name, user_id FROM user ORDER BY display_name ASC')

    return jsonify({
        'users': users
    }), 200

#####

@users_blueprint.route('/user', methods=['GET'])
def get_user_by_name():
    pass

@users_blueprint.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    GET /api/users/<user_id>

    Retrieve detailed information about a specific user

    RETURNS:
        user info with statistics (total msgs, rooms, subs, bits, recent activity)
    """

    user = query_db(
        'SELECT * FROM user WHERE user_id = ?', (user_id,), one=True
    )

    if not user:
        return jsonify({
            'error': 'Not found',
            'message': f'User {user_id} not found'
        }), 404
    
    msg_count = query_db(
        'SELECT COUNT(*) as count FROM privmsg WHERE user_id = ?', (user_id,), one=True
    )

    rooms = query_db('''
        SELECT
            r.room_id,
            r.room_name,
            COUNT(*) as msg_count
        FROM privmsg p
        JOIN room r ON p.room_id = r.room_id
        WHERE p.user_id = ?
        GROUP BY r.room_id
        ORDER BY msg_count DESC
    ''', (user_id,))

    sub_count = query_db(
        'SELECT COUNT(*) as count FROM sub WHERE user_id = ?', (user_id,), one=True
    )

    bits_total = query_db(
        'SELECT COALESCE(SUM(bits), 0) as total FROM bits WHERE user_id = ?', (user_id,), one=True
    )

    recent_messages = query_db('''
        SELECT
            p.*,
            r.room_name
        FROM privmsg p
        LEFT JOIN room r ON p.room_id = r.room_id
        WHERE p.user_id = ?
        ORDER BY p.timestamp DESC
        LIMIT 10
    ''', (user_id,))

    return jsonify({
        'user': user,
        'stats': {
            'total_messages': msg_count['count'],
            'total_subscriptions': sub_count['count'],
            'total_bits': bits_total['total'],
            'rooms_count': len(rooms)
        },
        'rooms': rooms,
        'recent_messages': recent_messages
    }), 200

@users_blueprint.route('/<user_id>/activity', methods=['GET'])
def get_user_activity(user_id):
    """
    GET /api/users/<user_id>/activity

    Retrieve user's activity timeline

    PARAMETERS:
        limit (int): max events to return
        type (str): filter by event type (message, sub, bits, raid)
    
    RETURNS:
        chronological list of user activities
    """

    limit = min(request.args.get('limit', default=50, type=int), 500)
    event_type = request.args.get('type', default=None, type=str)

    activities = []
    
    if not event_type or event_type == 'message':
        messages = query_db('''
            SELECT
                'message' as type,
                timestamp,
                room_id,
                msg_content as content,
                serial as id
            FROM privmsg
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
            ''', (user_id, limit))
        activities.extend(messages)

    if not event_type or event_type == 'sub':
        subs = query_db('''
            SELECT
                'subscription' as type,
                timestamp,
                room_id,
                system_msg as content,
                serial as id
            FROM sub
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
            ''', (user_id, limit))
        activities.extend(subs)

    if not event_type or event_type == 'bits':
        bits = query_db('''
            SELECT
                'bits' as type,
                timestamp,
                room_id,
                'Cheered ' || bits || ' bits' as content,
                serial as id
            FROM bits
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
            ''', (user_id, limit))
        activities.extend(bits)

    activities.sort(key=lambda x: x['timestamp'], reverse=True)

    activities = activities[:limit]

    return jsonify({
        'user_id': user_id,
        'activities': activities,
        'count': len(activities)
    }), 200
