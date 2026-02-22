from flask import Blueprint, jsonify, request
from ..models.database import query_db
from ..utils import utils

upgrade_blueprint = Blueprint('paidupgrades', __name__, url_prefix='/api/paidupgrades')

@upgrade_blueprint.route('/', methods=['GET'])
def get_paidupgrade():
    """
    GET /api/paidupgrades
    """
    try:
        user_name = request.args.get('user-name', default=None)
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
                    p.timestamp,
                    p.sub_plan,
                    p.sender_name,
                    u.display_name,
                    r.room_name
                FROM paidupgrade p
                LEFT JOIN user u ON p.user_id = u.user_id
                LEFT JOIN room r ON p.room_id = r.room_id
                WHERE 1=1
                '''
        
        params = []

        if user_name  is not None:
            query += ' AND LOWER (u.display_name) = LOWER(?)'
            params.append(user_name)
        
        if user_id is not None:
            query += ' AND u.user_id = ?'
            params.append(user_id)

        if room_name is not None:
            query += ' AND LOWER(r.room_name) = LOWER(?)'
            params.append(room_name)

        if room_id is not None:
            query += ' AND r.room_id = ?'
            params.append(room_id)

        if start_date is not None:
            query += ' AND p.timestamp >= ?'
            params.append(utils.parse_date(start_date))

        if end_date is not None:
            query += ' AND p.timestamp <= ?'
            params.append(utils.parse_date(end_date, end_of_day=True))

        query += ' ORDER BY p.timestamp DESC'
        query += ' LIMIT ? OFFSET ?'

        params.extend([limit, offset])

        paidupgrades = query_db(query, tuple(params))

        if paidupgrades is None:
            return jsonify({
                'error': ' No paid upgrades found matching the criteria.'
            }), 404
        
        return jsonify({
            'data': paidupgrades,
            'count': len(paidupgrades)
        }), 200

    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400