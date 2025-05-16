from flask import Blueprint, request, jsonify
from app import db
from app.models import Player
import jwt
from datetime import datetime, timedelta
from config import Config
from app.auth_utils import token_required
from app.routes import auth_bp

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('password'):
        return jsonify({'message': 'Name and password are required!'}), 400

    if Player.query.filter_by(name=data['name']).first():
        return jsonify({'message': 'Player with that name already exists!'}), 400

    new_player = Player(name=data['name'])
    new_player.set_password(data['password'])
    db.session.add(new_player)
    db.session.commit()

    return jsonify({'message': 'Registered successfully!'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    if not auth or not auth.get('name') or not auth.get('password'):
        return jsonify({'message': 'Name and password are required!'}), 401

    player = Player.query.filter_by(name=auth.get('name')).first()

    if not player or not player.check_password(auth.get('password')):
        return jsonify({'message': 'Invalid credentials!'}), 401

    token = jwt.encode({
        'player_id': player.id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, Config.SECRET_KEY, algorithm="HS256")

    return jsonify({'token': token})