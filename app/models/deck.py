from app import db
import enum
from sqlalchemy.types import Enum
import uuid
from sqlalchemy.dialects.postgresql import UUID

class DeckCategory(enum.Enum):
    ALGORITHMS = "algorithms"
    LANGUAGE = "language"
    MATH = "math"
    SYSTEM_DESIGN = "system design"

class Deck(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(Enum(DeckCategory, native_enum=False), nullable=False)
    card = db.relationship('Card', backref='deck', lazy=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
