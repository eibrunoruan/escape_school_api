from flask import jsonify
from app import db
from app.models import Puzzle, Room, PlayerRoomProgress, GameProgress, Badge, PlayerBadge
from app.auth_utils import token_required
from app.routes import game_data_bp

def _get_or_404(model: db.Model, resource_id: int):
    instance = model.query.get_or_404(resource_id)
    return instance

@game_data_bp.route('/puzzles', methods=['GET'])
@token_required
def get_puzzles(current_user):
    puzzles = Puzzle.query.all()
    return jsonify([puzzle.to_dict() for puzzle in puzzles]), 200

@game_data_bp.route('/puzzles/<int:puzzle_id>', methods=['GET'])
@token_required
def get_puzzle(puzzle_id, current_user):
    puzzle = _get_or_404(Puzzle, puzzle_id)
    return jsonify(puzzle.to_dict()), 200

@game_data_bp.route('/rooms', methods=['GET'])
@token_required
def get_rooms(current_user):
    rooms = Room.query.all()
    return jsonify([room.to_dict() for room in rooms]), 200

@game_data_bp.route('/rooms/<int:room_id>', methods=['GET'])
@token_required
def get_room(room_id, current_user):
    room = _get_or_404(Room, room_id)
    return jsonify(room.to_dict()), 200

@game_data_bp.route('/player_room_progress', methods=['GET'])
@token_required
def get_player_room_progress(current_user):
    progress = PlayerRoomProgress.query.all()
    return jsonify([p.to_dict() for p in progress]), 200

@game_data_bp.route('/player_room_progress/<int:progress_id>', methods=['GET'])
@token_required
def get_player_room_progress_by_id(progress_id, current_user):
    progress = _get_or_404(PlayerRoomProgress, progress_id)
    return jsonify(progress.to_dict()), 200

@game_data_bp.route('/player/<int:player_id>/room/<int:room_id>/progress', methods=['GET'])
@token_required
def get_player_room_progress_by_player_room(player_id, room_id, current_user):
    progress = PlayerRoomProgress.query.filter_by(player_id=player_id, room_id=room_id).first_or_404()
    return jsonify(progress.to_dict()), 200

@game_data_bp.route('/game_progress', methods=['GET'])
@token_required
def get_all_game_progress(current_user):
    progress = GameProgress.query.all()
    return jsonify([p.to_dict() for p in progress]), 200

@game_data_bp.route('/game_progress/<int:progress_id>', methods=['GET'])
@token_required
def get_game_progress(progress_id, current_user):
    progress = _get_or_404(GameProgress, progress_id)
    return jsonify(progress.to_dict()), 200

@game_data_bp.route('/player/<int:player_id>/game_progress', methods=['GET'])
@token_required
def get_player_game_progress(player_id, current_user):
    progress = GameProgress.query.filter_by(player_id=player_id).first_or_404()
    return jsonify(progress.to_dict()), 200

@game_data_bp.route('/badges', methods=['GET'])
@token_required
def get_badges(current_user):
    badges = Badge.query.all()
    return jsonify([badge.to_dict() for badge in badges]), 200

@game_data_bp.route('/badges/<int:badge_id>', methods=['GET'])
@token_required
def get_badge(badge_id, current_user):
    badge = _get_or_404(Badge, badge_id)
    return jsonify(badge.to_dict()), 200

@game_data_bp.route('/player_badges', methods=['GET'])
@token_required
def get_all_player_badges(current_user):
    player_badges = PlayerBadge.query.all()
    return jsonify([pb.to_dict() for pb in player_badges]), 200

@game_data_bp.route('/player_badges/<int:player_badge_id>', methods=['GET'])
@token_required
def get_player_badge(player_badge_id, current_user):
    player_badge = _get_or_404(PlayerBadge, player_badge_id)
    return jsonify(player_badge.to_dict()), 200

@game_data_bp.route('/player/<int:player_id>/badges', methods=['GET'])
@token_required
def get_player_badges(player_id, current_user):
    player_badges = PlayerBadge.query.filter_by(player_id=player_id).all()
    return jsonify([pb.to_dict() for pb in player_badges]), 200