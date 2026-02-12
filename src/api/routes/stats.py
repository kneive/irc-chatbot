from flask import Blueprint, jsonify, request
from ..models.database import query_db

stats_bluepint = Blueprint('stats', __name__, url_prefix='/api/stats')

@stats_blueprint.route('/overview', methods=['GET'])
def get_overview():
    """
    GET /api/stats/overview

    Retrieve statistics of the entire database

    RETURNS:
        JSON object
    """

    total_messages = query_db('SELECT COUNT(*) as count FROM privmsg', one=True)
    total_users = query_db('SELECT COUNT(*) as count FROM user', one=True)
    total_rooms = query_db('SELECT COUNT(*) as count FROM room', one=True)
    total_subs = query_db('SELECT COUNT(*) as count FROM sub', one=True)
    total_subgifts = query_db('SELECT COUNT(*) as count FROM subgift', one=True)
    total_bits = query_db('SELECT COALESCE(SUM(bits), 0) as total FROM bits', one=True)
    total_raids = query_db('SELECT COUNT(*) as count FROM raid', one=True)

    date_range = query_db('''SELECT
                                MIN(timestamp) as earliest,
                                MAX(timestamp) as latest
                              FROM privmsg
                          ''', one=True)
    
    return jsonify({
        'totals': {
            'messages': total_messages['count'],
            'users':total_users['count'],
            'rooms':total_rooms['count'],
            'subscriptions':total_subs['subs'],
            'subgifts':total_subgifts['count'],
            'bits':total_bits['total'],
            'raids':total_raids['count']
        },
        'date_range': date_range
    }), 200
