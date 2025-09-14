import jwt, datetime
from flask import request, jsonify
from functools import wraps
from config import Config

def generate_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not token:
                return jsonify({'message': 'Token missing'}), 401
            try:
                data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
                if role and data['role'] != role:
                    return jsonify({'message': 'Unauthorized'}), 403
                request.user = data
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token'}), 401
            return f(*args, **kwargs)
        return wrapper
    return decorator