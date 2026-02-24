from flask import Blueprint, jsonify, request
from ..models.database import query_db
from ..utils import utils

sub_blueprint = Blueprint('subscriptions', __name__, url_prefix='/api/subscriptions')

@sub_blueprint.route('/', methods=['GET'])
def get_subscriptions():
    """
    GET /api/subscriptions
    """

    try:

        room_name = request.args.get('room-name', default=None, type=str)
        room_id = request.args.get('room-id', default=None, type=int)
        user_name = request.args.get('user-name', default=None, type=str)
        user_id = request.args.get('user-id', default=None, type=int)
        start_date = request.args.get('start-date', default=None, type=str)
        end_date = request.args.get('end-date', default=None, type=str)

        limit = request.args.get('limit', default=500, type=int)
        offset = request.args.get('offset', default=0, type=int)

        limit = min(limit, 1000)    # upper limit per request

        query = '''
                SELECT
                    u.display_name, 
                    r.room_name,
                    s.sub_plan,
                    s.timestamp
                FROM sub s
                JOIN user u ON s.user_id = u.user_id
                JOIN room r ON s.room_id = r.room_id
                WHERE 1=1
                '''
        
        params = []

        if room_name is not None:
            query += ' AND r.room_name = ?'
            params.append(room_name)

        elif room_id is not None:
            query += ' AND r.room_id = ?'
            params.append(room_id)

        if user_name is not None:
            query += ' AND u.display_name = ?'
            params.append(user_name)
        
        if user_id is not None:
            query += ' AND u.user_id = ?'
            params.append(user_id)

        if start_date is not None:
            query += ' AND s.timestamp >= ?'
            params.append(utils.parse_date(start_date))

        if end_date is not None:
            query += ' AND s.timestamp <= ?'
            params.append(utils.parse_date(end_date, end_of_day=True))

        query += ' ORDER BY s.timestamp DESC'
        query += ' LIMIT ? OFFSET ?'

        params.extend([limit, offset])

        subs = query_db(query, tuple(params))

        if subs is None:
            return jsonify({
                'data': [],
                'count': 0,
                'limit': limit,
                'offset': offset,
                'hasMore': False
            }), 200
        
        return jsonify({
            'data': subs,
            'count': len(subs),
            'limit': limit,
            'offset': offset,
            'hasMore': len(subs) == limit
        }), 200
    
    except ValueError as e:
        return jsonify({
            'error' : str(e)
        }), 400