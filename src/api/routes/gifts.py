from flask import Blueprint, jsonify, request
from ..models import database
from ..utils import utils

gift_blueprint = Blueprint('mysterygifts', __name__, url_prefix='/api/mysterygifts')

@gift_blueprint.route('/', methods=['GET'])
def get_gifts():
    """
    GET /api/mysterygifts
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
                    u.display_name,
                    r.room_name,
                    g.sub_plan,
                    g.mass_gift_count,
                    g.timestamp
                FROM submysterygift g
                JOIN user u ON g.user_id = u.user_id
                JOIN room r ON g.room_id = r.room_id
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
            query += ' AND g.timestamp >= ?'
            params.append(parsed_date)

        if end_date is not None:
            parsed_date = utils.parse_date(end_date, end_of_day=True)
            query += ' AND g.timestamp <= ?'
            params.append(parsed_date)

        gifts = database.query_db(query, tuple(params))

        if gifts is None:
            return jsonify({
                'error': 'Not found',
                'message': 'No mystery gifts found matching the criteria.'
            }), 404
        
        return jsonify({
            'mystery_gifts': gifts,
            'count': len(gifts)
        }), 200

    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400