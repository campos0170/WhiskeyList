from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .database import db
from .models import WhiskeyBottle

whiskey_routes = Blueprint('whiskey_routes', __name__)

@whiskey_routes.route('/', methods=['GET'])
@jwt_required()
def get_whiskeys():
    user_id = get_jwt_identity()
    whiskeys = WhiskeyBottle.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            'id': whiskey.id,
            'name': whiskey.name,
            'distillery': whiskey.distillery,
            'age': whiskey.age,
            'type': whiskey.type,
            'proof': whiskey.proof
        }
        for whiskey in whiskeys
    ]), 200

@whiskey_routes.route('/', methods=['POST'])
@jwt_required()
def add_whiskey():
    data = request.get_json()
    user_id = get_jwt_identity()

    try:
        whiskey = WhiskeyBottle(
            name=data['name'],
            distillery=data['distillery'],
            age=data.get('age'),
            type=data['type'],
            proof=data['proof'],
            user_id=user_id
        )
        db.session.add(whiskey)
        db.session.commit()
        return jsonify({'message': 'Whiskey added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@whiskey_routes.route('/<int:whiskey_id>', methods=['PUT'])
@jwt_required()
def update_whiskey(whiskey_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    whiskey = WhiskeyBottle.query.filter_by(id=whiskey_id, user_id=user_id).first()

    if not whiskey:
        return jsonify({'message': 'Whiskey not found'}), 404

    whiskey.name = data.get('name', whiskey.name)
    whiskey.distillery = data.get('distillery', whiskey.distillery)
    whiskey.age = data.get('age', whiskey.age)
    whiskey.type = data.get('type', whiskey.type)
    whiskey.proof = data.get('proof', whiskey.proof)

    db.session.commit()
    return jsonify({'message': 'Whiskey updated successfully'}), 200

@whiskey_routes.route('/<int:whiskey_id>', methods=['DELETE'])
@jwt_required()
def delete_whiskey(whiskey_id):
    user_id = get_jwt_identity()
    whiskey = WhiskeyBottle.query.filter_by(id=whiskey_id, user_id=user_id).first()

    if not whiskey:
        return jsonify({'message': 'Whiskey not found'}), 404

    db.session.delete(whiskey)
    db.session.commit()
    return jsonify({'message': 'Whiskey deleted successfully'}), 200
