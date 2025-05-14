import datetime
import jwt

from functools import wraps
from flask import request, jsonify, Blueprint, current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    auth_data = request.get_json()
    username = auth_data.get('username')
    password = auth_data.get('password')

    if username == 'admin' and password == 'password':

        token = jwt.enconde(
            {
                'user': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)
    return decorated