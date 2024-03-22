from extensions import db
from datetime import datetime

class Guess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_round_id = db.Column(db.Integer, db.ForeignKey('game_round.id'), nullable=False)
    letters = db.Column(db.String(255), nullable=False)
    guessed_word = db.Column(db.String(255), nullable=True)  # This will be null if the player rerolled!

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
