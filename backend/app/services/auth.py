import firebase_admin
from firebase_admin import credentials, auth
from flask import request, jsonify
from functools import wraps
from app.config import Config
from app.models import User
from app.extensions import db
import os
print("Looking for key at:", Config.FIREBASE_KEY_PATH)
print("File exists:", os.path.exists(Config.FIREBASE_KEY_PATH))

# Initialize Firebase Admin SDK
try:
    cred = credentials.Certificate(Config.FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)
except ValueError:
    # Firebase already initialized
    pass

def verify_token():
    """
    Extracts and verifies Firebase token from request header.
    Returns the user's Firebase UID if valid, None if invalid.
    """
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.replace('Bearer ', '')
    
    try:
        decoded = auth.verify_id_token(token)
        uid = decoded['uid']
        email = decoded.get('email', '')
        
        # Create user in DB if first time logging in
        user = User.query.get(uid)
        if not user:
            user = User(id=uid, email=email)
            db.session.add(user)
            db.session.commit()
        
        return uid
    
    except Exception as e:
        print("\n========== FIREBASE TOKEN ERROR ==========")
        print("Error type:", type(e).__name__)
        print("Error:", e)
        print("Token (first 100 chars):", token[:100])
        print("=========================================\n")
        return None

def require_auth(f):
    """
    Decorator that checks token before route executes.
    Attaches verified user ID to request object.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        uid = verify_token()
        if not uid:
            return jsonify({"error": "Unauthorized"}), 401
        
        request.uid = uid  # attach to request for route to use
        return f(*args, **kwargs)
    
    return decorated