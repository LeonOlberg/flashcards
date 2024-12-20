from flask import Blueprint, request, jsonify
from app.models import db, Deck, DeckCategory

deck_bp = Blueprint('decks', __name__, url_prefix='/decks')

@deck_bp.route('', methods=['GET'])
def get_decks():
    decks = Deck.query.all()

    return jsonify([{
        "id": deck.id,
        "title": deck.title,
        "category": deck.category.value,
        "created_at": deck.created_at,
        "updated_at": deck.updated_at
    } for deck in decks])

@deck_bp.route('/<int:deck_id>', methods=['GET'])
def get_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    return jsonify({
        "id": deck.id,
        "title": deck.title,
        "category": deck.category.value
    })

@deck_bp.route('', methods=['POST'])
def create_deck():
    data = request.get_json()
    title = data['title']

    if not title:
        return jsonify({"error": "Title is required"}), 400

    category = data['category']
    if category not in DeckCategory._value2member_map_:
        return jsonify({"error": f"Invalid category. Valid categories are: {list(DeckCategory._value2member_map_.keys())}"}), 400

    new_deck = Deck(title=title, category=DeckCategory(category))
    db.session.add(new_deck)
    db.session.commit()

    return jsonify({
        "id": new_deck.id,
        "title": new_deck.title,
        "category": new_deck.category.value,
        "created_at": new_deck.created_at,
        "updated_at": new_deck.updated_at
    }), 201

@deck_bp.route('/<int:deck_id>', methods=['PATCH'])
def update_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    data = request.get_json()
    allowed_fields = {'title', 'category'}

    for field in allowed_fields:
        if field in data:
            if field == 'category':
                category = data['category']
                if category not in DeckCategory._value2member_map_:
                    return jsonify({
                        "error": f"Invalid category. Valid categories are: {list(DeckCategory._value2member_map_.keys())}"
                    }), 400
                deck.category = DeckCategory(category)
            else:
                setattr(deck, field, data[field])

    db.session.commit()

    return jsonify({
        "id": deck.id,
        "title": deck.title,
        "category": deck.category.value
    })

@deck_bp.route('/<int:deck_id>', methods=['DELETE'])
def delete_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    db.session.delete(deck)
    db.session.commit()

    return jsonify({"message": f"Deck {deck.title} deleted successfully"}), 200

