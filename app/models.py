from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    game_progress = db.relationship('GameProgress', backref='player', uselist=False)
    room_progress = db.relationship('PlayerRoomProgress', backref='player')
    badges = db.relationship('PlayerBadge', backref='player')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    type = db.Column(db.String(50)) # Ex: 'chave', 'ferramenta', 'consumivel'
    properties = db.Column(db.JSON) # Para armazenar propriedades específicas do item (ex: qual porta a chave abre, se a lanterna está ligada)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'properties': self.properties,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class PlayerItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantity = db.Column(db.Integer, default=1)
    acquired_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    db.UniqueConstraint('player_id', 'item_id', name='unique_player_item')

    def to_dict(self):
        return {
            'id': self.id,
            'player_id': self.player_id,
            'item_id': self.item_id,
            'quantity': self.quantity,
            'acquired_at': self.acquired_at.isoformat()
        }

class Puzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    solution = db.Column(db.String(255), nullable=False)
    reward = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    rooms = db.relationship('RoomPuzzle', backref='puzzle')
    player_room_progress = db.relationship('PlayerRoomPuzzle', backref='puzzle')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'solution': self.solution,
            'reward': self.reward,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    puzzles = db.relationship('RoomPuzzle', backref='room')
    player_progress = db.relationship('PlayerRoomProgress', backref='room')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class RoomPuzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    puzzle_id = db.Column(db.Integer, db.ForeignKey('puzzle.id'))
    order = db.Column(db.Integer) # Para definir a ordem dos enigmas na sala
    db.UniqueConstraint('room_id', 'puzzle_id', name='unique_room_puzzle')

class PlayerRoomProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    start_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    end_time = db.Column(db.DateTime)
    time_spent = db.Column(db.Integer) # em segundos
    puzzles_solved = db.relationship('PlayerRoomPuzzle', backref='player_room_progress')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    db.UniqueConstraint('player_id', 'room_id', name='unique_player_room')

    def to_dict(self):
        return {
            'id': self.id,
            'player_id': self.player_id,
            'room_id': self.room_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'time_spent': self.time_spent,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class PlayerRoomPuzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_room_progress_id = db.Column(db.Integer, db.ForeignKey('player_room_progress.id'))
    puzzle_id = db.Column(db.Integer, db.ForeignKey('puzzle.id'))
    solved_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    db.UniqueConstraint('player_room_progress_id', 'puzzle_id', name='unique_player_room_puzzle')

class GameProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), unique=True)
    current_room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    game_completed = db.Column(db.Boolean, default=False)
    completion_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'player_id': self.player_id,
            'current_room_id': self.current_room_id,
            'game_completed': self.game_completed,
            'completion_time': self.completion_time.isoformat() if self.completion_time else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(255))
    rule = db.Column(db.String(255)) # Ex: 'puzzles_solved >= 1'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    players = db.relationship('PlayerBadge', backref='badge')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'rule': self.rule,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class PlayerBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'))
    awarded_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    db.UniqueConstraint('player_id', 'badge_id', name='unique_player_badge')

    def to_dict(self):
        return {
            'id': self.id,
            'player_id': self.player_id,
            'badge_id': self.badge_id,
            'awarded_at': self.awarded_at.isoformat()
        }


