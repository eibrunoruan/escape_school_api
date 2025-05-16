from flask import Blueprint

main_bp = Blueprint('main', __name__)
game_data_bp = Blueprint('game_data', __name__, url_prefix='/game')
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

from app.routes import players, game_data, auth, admin