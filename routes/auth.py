from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import check_password_hash, generate_password_hash
from utils.jwt_utils import generate_token
from sqlalchemy.dialects.mysql import ENUM

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        token = generate_token(user.id, user.role)
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data.get('username') or not data.get('password') or not data.get('role'):
        return jsonify({'message': 'Missing required fields'}), 400

    if data['role'] not in ['Employee', 'Manager']:
        return jsonify({'message': 'Invalid role'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 409

    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_password, role=data['role'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})