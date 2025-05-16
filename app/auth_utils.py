import jwt
from flask import request, jsonify, abort
from functools import wraps
from config import Config
from app.models import Player

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token está faltando!'}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = Player.query.filter_by(id=data['player_id']).first()
        except:
            return jsonify({'message': 'Token é inválido!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    @token_required
    def decorated_function(current_user, *args, **kwargs):
        if not current_user.is_admin:
            abort(403, description="Acesso administrativo necessário.")
        return f(current_user, *args, **kwargs)
    return decorated_function