from flask import Blueprint, jsonify, request
from ..models.database import query_db, execute_db

msg_blueprint = Blueprint('messages', __name__, url_prefix='/api/privmsg')

@msg_blueprint.route('/', methods=['GET'])
def get_privmsgs():
    """
    GET /api/privmsg

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
    user = request.args.get('user_id', default=None, type=str)
    channel = request.args.get('room_id', default=None, type=str)

    # building SQL query with optional filters
    query = 'SELECT * FROM privmsg'
    conditions = []
    params = []

    # add WHERE conditions if filters are applied
    if user:
        conditions.append('user_id = ?')
        params.append(user)

    if channel:
        conditions.append('room_id = ?')
        params.append(channel)
    
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    # add ordering and pagination
    query += ' ORDER BY timestamp DESC LIMIT ? OFFSET ?'
    params.extend([limit, offset])

    # execute query
    privmsgs = query_db(query, tuple(params))

    # get total count
    count_query = 'SELECT COUNT(*) as count FROM privmsg'
    if conditions:
        count_query += ' WHERE ' + ' AND '.join(conditions)

    total = query_db(count_query, tuple(params[:-2]), one=True)['count']

    return jsonify({
        'data': privmsgs,
        'count': len(privmsgs),
        'total': total,
        'limit': limit,
        'offset': offset
    }), 200

@msg_blueprint.route('/<int:message_id>', methods=['GET'])
def get_privmsg(message_id):
    """
    GET /api/privmsg/<privmsg_id>
    
    Retrieve a single message by ID

    PARAMETERS
        message_id

    RETURN
        JSON object with message data or 404

    EXAMPLE
        GET /api/privmsg/42
    """

    privmsg = query_db(
        'SELECT * FROM privmsg WHERE serial = ?',
        (message_id,),
        one=True
    )

    if privmsg is None:
        return jsonify({
            'error': 'Not found',
            'message': f'Message with ID {message_id} does not exist'
        }), 404
    
    return jsonify({'data': privmsg}), 200

@msg_blueprint.route('/stats', methods=['GET'])
def get_privmsg_stats():
    """
    GET /api/privmsg/stats

    Retrieve statistics about messages

    RETURNS
        JSON object with
            total_messages: total number of messages
            unique_users: number of unique users
            messages_by_channel: number of messages per channel
            top_users: users with 50 most messages
    """

    total = query_db(
        'SELECT COUNT(*) as count FROM privmsg', 
        one=True
    )

    unique_users = query_db(
        'SELECT COUNT(DISTINCT user_id) AS count FROM privmsg', 
        one=True
    )

    by_channel = query_db('''
                    SELECT room_id, COUNT(*) as count
                    FROM privmsg
                    GROUP BY room_id
                    ORDER BY count DESC       
                ''')
    
    top_users = query_db('''
                    SELECT user_id, COUNT(*) as count
                    FROM privmsg
                    GROUP BY user_id
                    ORDER BY count DESC
                    LIMIT 50     
                ''')

    return jsonify({
        'total_messages': total['count'],
        'unique_users': unique_users['count'],
        'messages_by_channel': by_channel,
        'top_users': top_users
    }), 200

@msg_blueprint.route('/search', methods=['GET'])
def search_privmsgs():
    """
    GET /api/privmsg/search

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