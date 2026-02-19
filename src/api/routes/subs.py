from flask import Blueprint, jsonify, request
from ..models.database import query_db

subs_blueprint = Blueprint('subscriptions', __name__, url_prefix='/api/subscriptions')

@subs_blueprint.route('/', methods=['GET'])
def get_subscriptions():
    """
    GET /api/subscriptions
    """

    pass