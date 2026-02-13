from flask import Blueprint, jsonify, request
from ..models.database import query_db

stats_blueprint = Blueprint('stats', __name__, url_prefix='/api/stats')

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

@stats_blueprint.route('/subscriptions', methods=['GET'])
def get_subscription_stats():
    """
    GET /api/stats/subscriptions

    Retrieve subscription statistics

    RETURNS:
        JSON object
    """

    subs_by_plan = query_db('''
                            SELECT
                                sub_plan,
                                COUNT(*) as count
                            FROM sub
                            GROUP BY sub_plan
                            ORDER BY count DESC
                        ''')
    
    
    top_gifters = query_db('''
                           SELECT
                                sg.user_id,
                                u.display_name,
                                COUNT(*) as gifts_given
                           FROM subgift sg
                           LEFT JOIN user u ON sg.user_id = u.user_id
                           GROUP BY sg.user_id
                           ORDER BY gifts_given DESC
                           LIMIT 10
                        ''')
    
    top_recipients = query_db ('''
                               SELECT
                                    recipient_id,
                                    recipient_display_name,
                                    COUNT(*) as gifts_received
                               FROM subgift
                               GROUP BY recipient_id
                               ORDER BY gifts_received DESC
                               LIMIT 10
                            ''')
    
    mystery_gifts = query_db('''
                            SELECT
                                COUNT(*) as total_mystery_gifts,
                                SUM(mass_gift_count) as total_mystery_subs
                             FROM submysterygift
                        ''', one=True)
    
    subs_by_room = query_db('''
                            SELECT
                                s.room_id,
                                r.room_name,
                                COUNT(*) as sub_count
                            FROM sub s
                            LEFT JOIN room r ON s.room_id = r.room_id
                            GROUP BY s.room_id
                            ORDER BY sub_count DESC
                        ''')
    
    return jsonify({
        'subs_by_pla': subs_by_plan,
        'top_gifters': top_gifters,
        'top_recipients': top_recipients,
        'mystery_gifts': mystery_gifts,
        'subs_by_room': subs_by_room
    }), 200

@stats_blueprint.route('/bits', methods=['GET'])
def get_bits_stats():
    """
    GET /api/stats/bits

    Get bits statistics
    """

    total = query_db('SELECT SUM(bits) as total FROM bits', one=True)

    top_cheerers = query_db('''
                            SELECT
                                b.user_id,
                                u.display_name,
                                u.login,
                                SUM(b.bits) as total_bits,
                                COUNT(*) as cheer_count
                            FROM bits b
                            LEFT JOIN user u ON b.user_id = u.user_id
                            GROUP BY b.user_id
                            ORDER BY total_bits DESC
                            LIMIT 10
                        ''')
    
    bits_by_room = query_db('''
                            SELECT
                                b.room_id,
                                r.room_name,
                                SUM(b.bits) as total_bits
                                COUNT(*) as cheer_count
                            FROM bits b
                            LEFT JOIN room r ON  b.room_id = r.room_id
                            GROUP BY b.room_id
                            ORDER BY total_bits DESC
                        ''')
    
    return jsonify({
        'total_bits': total['total'],
        'top_cheerers': top_cheerers,
        'bits_by_room': bits_by_room
    })

@stats_blueprint.route('/raids', methods=['GET'])
def get_raid_stats():
    """
    GET /api/stats/raids

    Get raid statistics
    """

    total = query_db('SELECT COUNT(*) as count FROM raid', one=True)
    
    biggest_raids = query_db('''
                            SELECT
                                r.*,
                                rm.room_name
                            FROM raid r
                            LEFT JOIN room rm ON  r.room_id = rm.room_id
                            ORDER BY CAST(r.msg_param_viewerCount AS INTEGER) DESC
                            LIMIT 10
                        ''')
    
    return jsonify({
        'total_raids': total['count'],
        'biggest_raids': biggest_raids
    }), 200