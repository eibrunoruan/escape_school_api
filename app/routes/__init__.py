from flask import Blueprint

main_bp = Blueprint('main', __name__)
game_data_bp = Blueprint('game_data', __name__)

from app.routes import players
from app.routes import game_data