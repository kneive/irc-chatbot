from flask import Blueprint, jsonify, request
from ..models.database import query_db
from ..utils import utils

bits_blueprint = Blueprint('bits', __name__, url_prefix='/api/bits')

@bits_blueprint.route('/', methods=['GET'])
def get_bits():
    """
    GET /api/bits
    """

    try: 
        pass

    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400