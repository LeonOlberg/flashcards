from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Card(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    front = db.Column(db.String(255), nullable=False)
    back = db.Column(db.String(255), nullable=False)
    deck_id = db.Column(UUID(as_uuid=True), db.ForeignKey('deck.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class DrawnCard(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    card_id = db.Column(UUID(as_uuid=True), db.ForeignKey('card.id'), nullable=False)
    is_drawn = db.Column(db.Boolean, default=False, nullable=False)

