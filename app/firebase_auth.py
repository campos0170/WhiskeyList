from functools import wraps
from flask import request, jsonify
from firebase_admin import auth as firebase_auth
from .models import User
from .database import db

def firebase_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or malformed token"}), 401
        try:
            token = auth_header.split(" ")[1]
            decoded_token = firebase_auth.verify_id_token(token)
            uid = decoded_token["uid"]
            email = decoded_token.get("email", "")
            display_name = decoded_token.get("name", "")
            request.user = decoded_token

            # 🔄 Ensure user exists in local DB
            user = User.query.get(uid)
            if not user:
                
                first_name, *last_parts = display_name.split(" ")
                last_name = " ".join(last_parts) if last_parts else ""

                new_user = User(
                    id=uid,
                    first_name=first_name or "Firebase",
                    last_name=last_name or "User",
                    username=email, 
                    email=email,
                    password_hash="firebase_auth_user"  
                )
                db.session.add(new_user)
                db.session.commit()

        except Exception as e:
            return jsonify({"error": "Invalid or expired token", "details": str(e)}), 401

        return fn(*args, **kwargs)
    return wrapper
