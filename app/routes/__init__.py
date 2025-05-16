from flask import Blueprint

main_bp = Blueprint('main', __name__)
game_data_bp = Blueprint('game_data', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

from app.routes import players
from app.routes import game_data
from app.routes import auth
