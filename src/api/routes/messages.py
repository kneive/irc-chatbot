from flask import Blueprint, jsonify, request
from ..models.database import query_db

msg_blueprint = Blueprint('messages', __name__, url_prefix='/api/messages')

@msg_blueprint.route('/user_name/all', methods=['GET'])
def get_all_messages_for_user_by_name(user_name):
    """
    GET /api/messages/user_name/all
    """

    messages = query_db('''
                        SELECT 
                            u.display_name,
                            r.room_name,
                            m.msg_content,
                            m.reply_msg_body,
                            m.timestamp
                        FROM privmsg m
                        JOIN user u ON m.user_id = u.user_id
                        JOIN room r ON m.room_id = r.room_id
                        WHERE u.display_name = ?
                        ORDER BY m.timestamp DESC
                        ''', (user_name, room_name))
    
    if messages is None:
        return jsonify({
            'error': 'Not found',
            'message': f'No messages found for user {user_name}.'
        }), 404
    
    return jsonify({
        'messages': messages,
        'count': len(messages)
    })

@msg_blueprint.route('/<int:user_id>/all', methods=['GET'])
def get_all_messages_for_user_by_id(user_id):
    """
    GET /api/messages/<user_id>/all
    """

    messages = query_db('''
                        SELECT
                            u.display_name,
                            r.room_name,
                            m.msg_content,
                            m.reply_msg_body,
                            m.timestamp
                        FROM privmsg m
                        JOIN user u ON m.user_id = u.user_id
                        JOIN room r ON m.room_id = r.room_id
                        WHERE u.user_id = ?
                        ORDER BY m.timestamp DESC
                        ''', (user_id, room_name))
    
    if messages is None:
        return jsonify({
            'error': 'Not found',
            'message': f'No messages found for user ID {user_id}.'
        }), 404
    
    return jsonify({
        'messages': messages,
        'count': len(messages)
    })

@msg_blueprint.route('/room_name/all/user_name', methods=['GET'])
def get_all_messages_room_name_user_name(room_name, user_name):
    """
    GET /api/messages/room_name/all/user_name)
    """

    messages = query_db('''
                        SELECT
                            u.display_name,
                            r.room_name,
                            m.msg_content,
                            m.reply_msg_body,
                            m.timestamp
                        FROM privmsg m
                        JOIN user u ON m.user_id = u.user_id
                        JOIN room r ON m.room_id = r.room_id
                        WHERE r.room_name = ? AND u.display_name = ?
                        ORDER BY m.timestamp DESC
                        ''', (room_name, user_name))
    
    if messages is None:
        return jsonify({
            'error': 'Not found',
            'message': f'No messages found for user {user_name} in room {room_name}'
        }), 404
    
    return jsonify({
        'messages': messages,
        'count': len(messages)
    }), 200

@msg_blueprint.route('/room_name/all/<int:user_id>', methods=['GET'])
def get_all_messages_room_name_user_id(room_name, user_id):
    """
    GET /api/messages/room_name/all/<user_id>
    """

    messages = query_db('''
                        SELECT
                            u.display_name,
                            r.room_name,
                            m.msg_content,
                            m.reply_msg_body,
                            m.timestamp
                        FROM privmsg m
                        JOIN user u ON m.user_id = u.user_id
                        JOIN room r ON m.room_id = r.room_id
                        WHERE r.room_name = ? AND u.user_id = ?
                        ORDER BY m.timestamp DESC
                        ''', (room_name, user_id))
    
    if messages is None:
        return jsonify({
            'error': 'Not found',
            'message': f'No messages found for user ID {user_id} in room {room_name}.'
        }), 404
    
    return jsonify({
        'messages': messages,
        'count': len(messages)
    }), 200

@msg_blueprint.route('/<int:room_id>/all/user_name', methods=['GET'])
def get_all_messages_room_id_user_name(room_id, user_name):
    """
    GET /api/messages/<room_id>/all/user_name
    """

    messages = query_db('''
                        SELECT
                            u.display_name,
                            r.room_name,
                            m.msg_content,
                            m.reply_msg_body,
                            m.timestamp
                        FROM privmsg m
                        JOIN user u ON m.user_id = u.user_id
                        JOIN room r ON m.room_id = r.room_id
                        WHERE r.room_id = ? AND u.display_name = ?
                        ORDER BY m.timestamp DESC
                        ''', (room_id, user_name))
    
    if messages is None:
        return jsonify({
            'error':'Not found',
            'messages': f'No messages found for user {user_name} in room ID {room_id}.'
        }), 404
    
    return jsonify({
        'messages': messages,
        'count': len(messages)
    }), 200


@msg_blueprint.route('/<int:room_id>/all/<int:user_id>', methods=['GET'])
def get_all_messages_room_id_user_id(room_id, user_id):
    """
    GET /api/messages/<room_id>/all/<user_id>
    """

    messages = query_db('''
                        SELECT
                            u.display_name,
                            r.room_name,
                            m.msg_content,
                            m.reply_msg_body,
                            m.timestamp
                        FROM privmsg m
                        JOIN user u ON m.user_id = u.user_id
                        JOIN room r ON m.room_id = r.room_id
                        WHERE r.room_id = ? AND u.user_id = ?
                        ORDER BY m.timestamp DESC
                        ''', (room_id, user_id))
    
    if messages is None:
        return jsonify({
            'error': 'Not found',
            'message': f'No messages found for user ID {user_id} in room ID {room_id}.'
        }), 404
    
    return jsonify({
        'messages': messages,
        'count': len(messages)
    }), 200