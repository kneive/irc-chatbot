import sqlite3
from flask import g, current_app
from typing import Any, Dict, List, Optional
from datetime import datetime

def get_db():
    """
    Get database connection
    """
    # g object stores connection during request, 1 connection per request, auto cleanup, thread safe
    # returns rows as dictionaries

    if 'db' not in g:

        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """
    Close database connection
    """

    db = g.pop('db', None)
    if db is not None:
        db.close()

def query_db(query:str, args:tuple=(), one:bool=False) -> Optional[Dict[str, Any]]:
    """
    Execute a database query
    
    PARAMETER:
    query: SQL query string with ? for parameters
    args: tuple of parameters to substitute
    one: flag whether to return only the first or all results

    RETURNS:
    List of dictionaries (if one=False)
    single dictionary (if one=True)
    None if no results
    """

    cursor = get_db().execute(query, args)
    data = cursor.fetchall()
    cursor.close()

    results = [dict(row) for row in data]

    return results[0] if one else results

def execute_db(query:str, args:tuple=())->int:
    """
    Execute a database query to modify data, i.e. INSERT, UPDATE, DELETE

    PARAMETERS:
    query: SQL query string with ? for parameters
    args: tuple of parameters to substitute

    RETURNS:
    ID of the last inserted row or number of affected rows
    """

    db=get_db()
    cursor = db.execute(query, args)
    db.commit()
    return cursor.lastrowid if query.strip().upper().startswith('INSERT') else cursor.rowcount

def init_app(app):
    """
    Register database functions with Flask app. Ensures close_db() is called after each request.
    """
    app.teardown_appcontext(close_db)


# utility functions
def get_user_by_id(user_id:str) -> Optional[Dict]:
    """Get user by id"""
    return query_db(
        'SELECT * FROM user WHERE user_id = ?', (user_id,), one=True
    )

def get_room_by_id(room_id:str) -> Optional[Dict]:
    """Get room by id"""
    return query_db(
        'SELECT * FROM room WHERE room_id = ?', (room_id,), one=True
    )

def get_user_display_name(user_id:str) -> Optional[str]:
    """Get user's display name by user_id"""
    user = get_user_by_id(user_id)
    return user['display_name'] if user else None

def get_room_name(room_id:str) -> Optional[str]:
    """Get room name by room_id"""
    room = get_room_by_id(room_id)
    return room['room_name'] if room else None