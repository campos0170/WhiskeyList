# app/auth.py
from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route('/ping', methods=['GET'])
def ping():
    return {'message': 'Auth service active'}, 200
