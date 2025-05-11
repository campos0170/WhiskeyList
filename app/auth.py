from flask import Blueprint, request, jsonify
from .models import User
from .database import db
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([first_name, last_name, username, email, password]):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter((User.email == email) | (User.username == username)).first():
        return jsonify({'error': 'Email or username already exists'}), 409

    user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200

    return jsonify({'error': 'Invalid email or password'}), 401
