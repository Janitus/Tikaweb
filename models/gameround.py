from extensions import db
from datetime import datetime

class GameRound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    player = db.relationship('User', backref=db.backref('game_rounds', lazy=True))
    guesses = db.relationship('Guess', backref='game_round', lazy=True)
