
from flask import Blueprint, request, jsonify
from .models import WhiskeyBottle
from .database import db
from .firebase_auth import firebase_required

whiskey_routes = Blueprint("whiskey_routes", __name__)

@whiskey_routes.route("/", methods=["GET"])
@firebase_required
def get_whiskeys():
    user_id = request.user["uid"]
    print(f"[GET] Fetching whiskeys for user_id: {user_id}")
    
    whiskeys = WhiskeyBottle.query.filter_by(user_id=user_id).all()
    print(f"[GET] Found {len(whiskeys)} whiskeys for user_id: {user_id}")

    return jsonify([
        {
            "id": w.id,
            "name": w.name,
            "distillery": w.distillery,
            "age": w.age,
            "type": w.type,
            "proof": w.proof,
        } for w in whiskeys
    ]), 200

@whiskey_routes.route("/", methods=["POST"])
@firebase_required
def add_whiskey():
    data = request.get_json()
    user_id = request.user["uid"]
    print(f"[POST] Adding whiskey for user_id: {user_id}")
    print(f"[POST] Received data: {data}")

    try:
        whiskey = WhiskeyBottle(
            name=data['name'],
            distillery=data['distillery'],
            age=int(data['age']) if data.get('age') else None,
            type=data['type'],
            proof=float(data['proof']) if data.get('proof') else None,
            user_id=user_id
        )
        db.session.add(whiskey)
        db.session.commit()

        print(f"[POST] Whiskey added with ID: {whiskey.id} for user_id: {user_id}")

        return jsonify({
            "id": whiskey.id,
            "name": whiskey.name,
            "distillery": whiskey.distillery,
            "age": whiskey.age,
            "type": whiskey.type,
            "proof": whiskey.proof,
            "user_id": whiskey.user_id
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"[POST] Error: {e}")
        return jsonify({'error': str(e)}), 500

@whiskey_routes.route("/<int:whiskey_id>", methods=["PUT"])
@firebase_required
def update_whiskey(whiskey_id):
    user_id = request.user["uid"]
    print(f"[PUT] Updating whiskey ID {whiskey_id} for user_id: {user_id}")

    whiskey = WhiskeyBottle.query.filter_by(id=whiskey_id, user_id=user_id).first()
    if not whiskey:
        print("[PUT] Whiskey not found or unauthorized access.")
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    whiskey.name = data.get("name", whiskey.name)
    whiskey.distillery = data.get("distillery", whiskey.distillery)
    whiskey.age = data.get("age", whiskey.age)
    whiskey.type = data.get("type", whiskey.type)
    whiskey.proof = data.get("proof", whiskey.proof)
    db.session.commit()

    print(f"[PUT] Whiskey ID {whiskey_id} updated.")

    return jsonify({"message": "Updated"}), 200

@whiskey_routes.route("/<int:whiskey_id>", methods=["DELETE"])
@firebase_required
def delete_whiskey(whiskey_id):
    user_id = request.user["uid"]
    print(f"[DELETE] Attempting to delete whiskey ID {whiskey_id} for user_id: {user_id}")

    whiskey = WhiskeyBottle.query.filter_by(id=whiskey_id, user_id=user_id).first()
    if not whiskey:
        print("[DELETE] Whiskey not found or unauthorized access.")
        return jsonify({"error": "Not found"}), 404

    db.session.delete(whiskey)
    db.session.commit()

    print(f"[DELETE] Whiskey ID {whiskey_id} deleted for user_id: {user_id}")

    return jsonify({"message": "Deleted"}), 200
