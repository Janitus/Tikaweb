from extensions import db
from datetime import datetime

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_round_id = db.Column(db.Integer, db.ForeignKey('game_round.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('scores', lazy=True))
    game_round = db.relationship('GameRound', backref=db.backref('scores', lazy=True))
