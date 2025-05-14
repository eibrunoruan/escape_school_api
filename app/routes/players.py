from flask import jsonify, request, abort
from app import db
from app.models import Player
from app.routes import main_bp
from app.auth import token_required

@main_bp.route('/players', methods=['GET'])
@token_required
def get_players(current_user):
    player_id = request.args.get('player_id')

    if player_id:
        try:
            player = Player.query.get_or_404(player_id)
            return jsonify(player.to_dict()), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        try:
            players = Player.query.all()
            return jsonify([player.to_dict() for player in players]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@main_bp.route('/players', methods=['POST'])
@token_required
def create_player(current_user):
    try:
        data = request.get_json() or {}
        if 'name' not in data:
            return jsonify({'error': 'name is required'}), 400
        if Player.query.filter_by(name=data['name']).first():
            return jsonify({'error': 'player name already exists'}), 400

        player = Player(name=data['name'])
        db.session.add(player)
        db.session.commit()

        return jsonify(player.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
