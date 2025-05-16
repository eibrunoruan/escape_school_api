from flask import jsonify, request, abort, Blueprint
from app import db
from app.models import Puzzle, Room, PlayerRoomProgress, GameProgress, Badge, PlayerBadge
from app.routes import game_data_bp
from app.auth_utils import token_required

@game_data_bp.route('/puzzles', methods=['GET'])
@token_required
def get_puzzles(current_user):
    puzzles = Puzzle.query.all()
    return jsonify([puzzle.to_dict() for puzzle in puzzles]), 200

@game_data_bp.route('/puzzles/<int:puzzle_id>', methods=['GET'])
@token_required
def get_puzzle(puzzle_id, current_user):
    puzzle = Puzzle.query.get_or_404(puzzle_id)
    return jsonify(puzzle.to_dict()), 200

@game_data_bp.route('/puzzles', methods=['POST'])
@token_required
def create_puzzle(current_user):
    data = request.get_json() or {}
    if 'name' not in data or 'description' not in data or 'solution' not in data:
        return jsonify({'error': 'name, description, and solution are required'}), 400
    puzzle = Puzzle(name=data['name'], description=data['description'], solution=data['solution'], reward=data.get('reward'))
    db.session.add(puzzle)
    db.session.commit()
    return jsonify(puzzle.to_dict()), 201

@game_data_bp.route('/puzzles/<int:puzzle_id>', methods=['PUT'])
@token_required
def update_puzzle(puzzle_id, current_user):
    puzzle = Puzzle.query.get_or_404(puzzle_id)
    data = request.get_json() or {}
    puzzle.name = data.get('name', puzzle.name)
    puzzle.description = data.get('description', puzzle.description)
    puzzle.solution = data.get('solution', puzzle.solution)
    puzzle.reward = data.get('reward', puzzle.reward)
    db.session.commit()
    return jsonify(puzzle.to_dict()), 200

@game_data_bp.route('/puzzles/<int:puzzle_id>', methods=['DELETE'])
@token_required
def delete_puzzle(puzzle_id, current_user):
    puzzle = Puzzle.query.get_or_404(puzzle_id)
    db.session.delete(puzzle)
    db.session.commit()
    return jsonify({'message': 'Puzzle deleted'}), 200

# Rotas para Room
@game_data_bp.route('/rooms', methods=['GET'])
@token_required
def get_rooms(current_user):
    rooms = Room.query.all()
    return jsonify([room.to_dict() for room in rooms]), 200

@game_data_bp.route('/rooms/<int:room_id>', methods=['GET'])
@token_required
def get_room(room_id, current_user):
    room = Room.query.get_or_404(room_id)
    return jsonify(room.to_dict()), 200

@game_data_bp.route('/rooms', methods=['POST'])
@token_required
def create_room(current_user):
    data = request.get_json() or {}
    if 'name' not in data:
        return jsonify({'error': 'name is required'}), 400
    room = Room(name=data['name'], description=data.get('description'))
    db.session.add(room)
    db.session.commit()
    return jsonify(room.to_dict()), 201

@game_data_bp.route('/rooms/<int:room_id>', methods=['PUT'])
@token_required
def update_room(room_id, current_user):
    room = Room.query.get_or_404(room_id)
    data = request.get_json() or {}
    room.name = data.get('name', room.name)
    room.description = data.get('description', room.description)
    db.session.commit()
    return jsonify(room.to_dict()), 200

@game_data_bp.route('/rooms/<int:room_id>', methods=['DELETE'])
@token_required
def delete_room(room_id, current_user):
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    return jsonify({'message': 'Room deleted'}), 200

# Rotas para PlayerRoomProgress
@game_data_bp.route('/player_room_progress', methods=['GET'])
@token_required
def get_player_room_progress(current_user):
    progress = PlayerRoomProgress.query.all()
    return jsonify([p.to_dict() for p in progress]), 200

@game_data_bp.route('/player_room_progress/<int:progress_id>', methods=['GET'])
@token_required
def get_player_room_progress_by_id(progress_id, current_user):
    progress = PlayerRoomProgress.query.get_or_404(progress_id)
    return jsonify(progress.to_dict()), 200

@game_data_bp.route('/player/<int:player_id>/room/<int:room_id>/progress', methods=['GET'])
@token_required
def get_player_room_progress_by_player_room(player_id, room_id, current_user):
    progress = PlayerRoomProgress.query.filter_by(player_id=player_id, room_id=room_id).first_or_404()
    return jsonify(progress.to_dict()), 200

@game_data_bp.route('/player_room_progress', methods=['POST'])
@token_required
def create_player_room_progress(current_user):
    data = request.get_json() or {}
    if 'player_id' not in data or 'room_id' not in data:
        return jsonify({'error': 'player_id and room_id are required'}), 400
    progress = PlayerRoomProgress(player_id=data['player_id'], room_id=data['room_id'])
    db.session.add(progress)
    db.session.commit()
    return jsonify(progress.to_dict()), 201

@game_data_bp.route('/player_room_progress/<int:progress_id>', methods=['PUT'])
@token_required
def update_player_room_progress(progress_id, current_user):
    progress = PlayerRoomProgress.query.get_or_404(progress_id)
    data = request.get_json() or {}
    progress.end_time = data.get('end_time')
    progress.time_spent = data.get('time_spent')
    db.session.commit()
    return jsonify(progress.to_dict()), 200

@game_data_bp.route('/player_room_progress/<int:progress_id>', methods=['DELETE'])
@token_required
def delete_player_room_progress(progress_id, current_user):
    progress = PlayerRoomProgress.query.get_or_404(progress_id)
    db.session.delete(progress)
    db.session.commit()
    return jsonify({'message': 'Player room progress deleted'}), 200

# Rotas para GameProgress
@game_data_bp.route('/game_progress', methods=['GET'])
@token_required
def get_all_game_progress(current_user):
    progress = GameProgress.query.all()
    return jsonify([p.to_dict() for p in progress]), 200

@game_data_bp.route('/game_progress/<int:progress_id>', methods=['GET'])
@token_required
def get_game_progress(progress_id, current_user):
    progress = GameProgress.query.get_or_404(progress_id)
    return jsonify(progress.to_dict()), 200

@game_data_bp.route('/player/<int:player_id>/game_progress', methods=['GET'])
@token_required
def get_player_game_progress(player_id, current_user):
    progress = GameProgress.query.filter_by(player_id=player_id).first_or_404()
    return jsonify(progress.to_dict()), 200

@game_data_bp.route('/game_progress', methods=['POST'])
@token_required
def create_game_progress(current_user):
    data = request.get_json() or {}
    if 'player_id' not in data:
        return jsonify({'error': 'player_id is required'}), 400
    # Certifique-se de que não existe progresso para este jogador
    if GameProgress.query.filter_by(player_id=data['player_id']).first():
        return jsonify({'error': 'Game progress already exists for this player'}), 400
    progress = GameProgress(player_id=data['player_id'], current_room_id=data.get('current_room_id'), game_completed=data.get('game_completed', False), completion_time=data.get('completion_time'))
    db.session.add(progress)
    db.session.commit()
    return jsonify(progress.to_dict()), 201

@game_data_bp.route('/game_progress/<int:progress_id>', methods=['PUT'])
@token_required
def update_game_progress(progress_id, current_user):
    progress = GameProgress.query.get_or_404(progress_id)
    data = request.get_json() or {}
    progress.current_room_id = data.get('current_room_id', progress.current_room_id)
    progress.game_completed = data.get('game_completed', progress.game_completed)
    progress.completion_time = data.get('completion_time', progress.completion_time)
    db.session.commit()
    return jsonify(progress.to_dict()), 200

@game_data_bp.route('/game_progress/<int:progress_id>', methods=['DELETE'])
@token_required
def delete_game_progress(progress_id, current_user):
    progress = GameProgress.query.get_or_404(progress_id)
    db.session.delete(progress)
    db.session.commit()
    return jsonify({'message': 'Game progress deleted'}), 200

# Rotas para Badge
@game_data_bp.route('/badges', methods=['GET'])
@token_required
def get_badges(current_user):
    badges = Badge.query.all()
    return jsonify([badge.to_dict() for badge in badges]), 200

@game_data_bp.route('/badges/<int:badge_id>', methods=['GET'])
@token_required
def get_badge(badge_id, current_user):
    badge = Badge.query.get_or_404(badge_id)
    return jsonify(badge.to_dict()), 200

@game_data_bp.route('/badges', methods=['POST'])
@token_required
def create_badge(current_user):
    data = request.get_json() or {}
    if 'name' not in data or 'description' not in data or 'rule' not in data:
        return jsonify({'error': 'name, description, and rule are required'}), 400
    badge = Badge(name=data['name'], description=data['description'], rule=data['rule'])
    db.session.add(badge)
    db.session.commit()
    return jsonify(badge.to_dict()), 201

@game_data_bp.route('/badges/<int:badge_id>', methods=['PUT'])
@token_required
def update_badge(badge_id, current_user):
    badge = Badge.query.get_or_404(badge_id)
    data = request.get_json() or {}
    badge.name = data.get('name', badge.name)
    badge.description = data.get('description', badge.description)
    badge.rule = data.get('rule', badge.rule)
    db.session.commit()
    return jsonify(badge.to_dict()), 200

@game_data_bp.route('/badges/<int:badge_id>', methods=['DELETE'])
@token_required
def delete_badge(badge_id, current_user):
    badge = Badge.query.get_or_404(badge_id)
    db.session.delete(badge)
    db.session.commit()
    return jsonify({'message': 'Badge deleted'}), 200

# Rotas para PlayerBadge
@game_data_bp.route('/player_badges', methods=['GET'])
@token_required
def get_all_player_badges(current_user):
    player_badges = PlayerBadge.query.all()
    return jsonify([pb.to_dict() for pb in player_badges]), 200

@game_data_bp.route('/player_badges/<int:player_badge_id>', methods=['GET'])
@token_required
def get_player_badge(player_badge_id, current_user):
    player_badge = PlayerBadge.query.get_or_404(player_badge_id)
    return jsonify(player_badge.to_dict()), 200

@game_data_bp.route('/player/<int:player_id>/badges', methods=['GET'])
@token_required
def get_player_badges(player_id, current_user):
    player_badges = PlayerBadge.query.filter_by(player_id=player_id).all()
    return jsonify([pb.to_dict() for pb in player_badges]), 200

@game_data_bp.route('/player_badges', methods=['POST'])
@token_required
def create_player_badge(current_user):
    data = request.get_json() or {}
    if 'player_id' not in data or 'badge_id' not in data:
        return jsonify({'error': 'player_id and badge_id are required'}), 400
    # Verificar se o jogador já possui essa badge
    if PlayerBadge.query.filter_by(player_id=data['player_id'], badge_id=data['badge_id']).first():
        return jsonify({'error': 'Player already has this badge'}), 400
    player_badge = PlayerBadge(player_id=data['player_id'], badge_id=data['badge_id'])
    db.session.add(player_badge)
    db.session.commit()
    return jsonify(player_badge.to_dict()), 201

@game_data_bp.route('/player_badges/<int:player_badge_id>', methods=['DELETE'])
@token_required
def delete_player_badge(player_badge_id, current_user):
    player_badge = PlayerBadge.query.get_or_404(player_badge_id)
    db.session.delete(player_badge)
    db.session.commit()
    return jsonify({'message': 'Player badge removed'}), 200