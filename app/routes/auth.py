from flask import request, jsonify
from app import db
from app.models import Player
import jwt
from datetime import datetime, timedelta, timezone
from config import Config
from app.routes import auth_bp
from sqlalchemy.exc import IntegrityError

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username e senha são obrigatórios!'}), 400
    try:
        new_player = Player(username=data['username'], name=data.get('name', ''))
        new_player.set_password(data['password'])
        db.session.add(new_player)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Jogador com este username já existe!'}), 400
    return jsonify({'message': 'Registrado com sucesso!'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Username e senha são obrigatórios!'}), 401
    player = Player.query.filter_by(username=auth.get('username')).first()
    if not player or not player.check_password(auth.get('password')):
        return jsonify({'message': 'Credenciais inválidas!'}), 401
    token = jwt.encode(
        {
            'player_id': player.id,
            'exp': int((datetime.now(timezone.utc) + timedelta(hours=24)).timestamp()),
        },
        Config.SECRET_KEY,
        algorithm='HS256',
    )
    return jsonify({'token': token}), 200