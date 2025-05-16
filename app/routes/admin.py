from flask import jsonify, request, abort
from app import db
from app.models import Puzzle, Room, Badge, PlayerBadge, PlayerRoomProgress, GameProgress, Player
from app.auth_utils import admin_required
from sqlalchemy.exc import IntegrityError
from app.routes import admin_bp

def _create_resource(model: db.Model, data: dict, required_fields: list[str]):
    for field in required_fields:
        if field not in data:
            abort(400, description=f"{field} é obrigatório")
    try:
        instance = model(**data)
        db.session.add(instance)
        db.session.commit()
        return jsonify(instance.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        abort(400, description=f"Já existe com estes dados")

def _update_resource(model: db.Model, resource_id: int, data: dict):
    instance = model.query.get_or_404(resource_id)
    for key, value in data.items():
        if hasattr(instance, key):
            setattr(instance, key, value)
    db.session.commit()
    return jsonify(instance.to_dict()), 200

def _delete_resource(model: db.Model, resource_id: int):
    instance = model.query.get_or_404(resource_id)
    db.session.delete(instance)
    db.session.commit()
    return jsonify({'message': f"{model.__name__} excluído"}), 200

@admin_bp.route('/superadmin', methods=['POST'])
@admin_required
def create_superadmin(current_user):
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        abort(400, description='Username e senha são obrigatórios para criar um superadmin.')

    username = data['username']
    password = data['password']

    if Player.query.filter_by(username=username).first():
        abort(400, description=f'Jogador com o username "{username}" já existe.')

    try:
        new_superadmin = Player(username=username, is_admin=True)
        new_superadmin.set_password(password)
        db.session.add(new_superadmin)
        db.session.commit()
        return jsonify({'message': f'Superadministrador "{username}" criado com sucesso!'}), 201
    except IntegrityError:
        db.session.rollback()
        abort(400, description='Erro ao criar o superadministrador.')

@admin_bp.route('/puzzles', methods=['POST'])
@admin_required
def create_puzzle(current_user):
    return _create_resource(Puzzle, request.get_json() or {}, ['name', 'description', 'solution'])

@admin_bp.route('/puzzles/<int:puzzle_id>', methods=['PUT'])
@admin_required
def update_puzzle(puzzle_id, current_user):
    return _update_resource(Puzzle, puzzle_id, request.get_json() or {})

@admin_bp.route('/puzzles/<int:puzzle_id>', methods=['DELETE'])
@admin_required
def delete_puzzle(puzzle_id, current_user):
    return _delete_resource(Puzzle, puzzle_id)

@admin_bp.route('/rooms', methods=['POST'])
@admin_required
def create_room(current_user):
    return _create_resource(Room, request.get_json() or {}, ['name'])

@admin_bp.route('/rooms/<int:room_id>', methods=['PUT'])
@admin_required
def update_room(room_id, current_user):
    return _update_resource(Room, room_id, request.get_json() or {})

@admin_bp.route('/rooms/<int:room_id>', methods=['DELETE'])
@admin_required
def delete_room(room_id, current_user):
    return _delete_resource(Room, room_id)

@admin_bp.route('/badges', methods=['POST'])
@admin_required
def create_badge(current_user):
    return _create_resource(Badge, request.get_json() or {}, ['name', 'description', 'rule'])

@admin_bp.route('/badges/<int:badge_id>', methods=['PUT'])
@admin_required
def update_badge(badge_id, current_user):
    return _update_resource(Badge, badge_id, request.get_json() or {})

@admin_bp.route('/badges/<int:badge_id>', methods=['DELETE'])
@admin_required
def delete_badge(badge_id, current_user):
    return _delete_resource(Badge, badge_id)

@admin_bp.route('/player_badges', methods=['POST'])
@admin_required
def create_player_badge(current_user):
    data = request.get_json() or {}
    if 'player_id' not in data or 'badge_id' not in data:
        abort(400, description='player_id e badge_id são obrigatórios')
    if PlayerBadge.query.filter_by(player_id=data['player_id'], badge_id=data['badge_id']).first():
        abort(400, description='Jogador já possui este badge')
    return _create_resource(PlayerBadge, data, ['player_id', 'badge_id'])

@admin_bp.route('/player_badges/<int:player_badge_id>', methods=['DELETE'])
@admin_required
def delete_player_badge(player_badge_id, current_user):
    return _delete_resource(PlayerBadge, player_badge_id)

@admin_bp.route('/player_room_progress', methods=['POST'])
@admin_required
def create_player_room_progress(current_user):
    return _create_resource(PlayerRoomProgress, request.get_json() or {}, ['player_id', 'room_id'])

@admin_bp.route('/player_room_progress/<int:progress_id>', methods=['PUT'])
@admin_required
def update_player_room_progress(progress_id, current_user):
    return _update_resource(PlayerRoomProgress, progress_id, request.get_json() or {})

@admin_bp.route('/player_room_progress/<int:progress_id>', methods=['DELETE'])
@admin_required
def delete_player_room_progress(progress_id, current_user):
    return _delete_resource(PlayerRoomProgress, progress_id)

@admin_bp.route('/game_progress', methods=['POST'])
@admin_required
def create_game_progress(current_user):
    data = request.get_json() or {}
    if 'player_id' not in data:
        abort(400, description='player_id é obrigatório')
    if GameProgress.query.filter_by(player_id=data['player_id']).first():
        abort(400, description='Progresso de jogo já existe para este jogador')
    return _create_resource(GameProgress, data, ['player_id'])

@admin_bp.route('/game_progress/<int:progress_id>', methods=['PUT'])
@admin_required
def update_game_progress(progress_id, current_user):
    return _update_resource(GameProgress, progress_id, request.get_json() or {})

@admin_bp.route('/game_progress/<int:progress_id>', methods=['DELETE'])
@admin_required
def delete_game_progress(progress_id, current_user):
    return _delete_resource(GameProgress, progress_id)