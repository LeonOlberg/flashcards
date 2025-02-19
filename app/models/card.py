from app import db

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(255), nullable=False)
    back = db.Column(db.String(255), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class DrawnCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    is_drawn = db.Column(db.Boolean, default=False, nullable=False)

