from flask import jsonify, request, abort
from app import db
from app.models import Player
from app.routes import main_bp
from app.auth_utils import token_required

@main_bp.route('/players', methods=['GET'])
@token_required
def get_players(current_user):
    player_id = request.args.get('player_id', type=int)
    if player_id:
        player = Player.query.get_or_404(player_id)
        return jsonify(player.to_dict()), 200
    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        players = Player.query.paginate(page=page, per_page=per_page)
        result = [p.to_dict() for p in players.items]
        return jsonify({
            'jogadores': result,
            'total': players.total,
            'paginas': players.pages,
            'pagina_atual': players.page
        }), 200

@main_bp.route('/players/<int:player_id>', methods=['PUT'])
@token_required
def update_player(current_user, player_id):
    player_to_update = Player.query.get_or_404(player_id)
    if current_user.id != player_to_update.id:
        abort(403, description="Você não tem permissão para atualizar este jogador.")

    data = request.get_json() or {}

    for key, value in data.items():
        if hasattr(player_to_update, key):
            setattr(player_to_update, key, value)

    db.session.commit()
    return jsonify(player_to_update.to_dict()), 200

@main_bp.route('/players/<int:player_id>', methods=['DELETE'])
@token_required
def delete_player(current_user, player_id):
    player_to_delete = Player.query.get_or_404(player_id)
    if current_user.id != player_to_delete.id:
        abort(403, description="Você não tem permissão para deletar este jogador.")

    db.session.delete(player_to_delete)
    db.session.commit()
    return jsonify({'message': f'Jogador com id {player_id} excluído com sucesso'}), 200