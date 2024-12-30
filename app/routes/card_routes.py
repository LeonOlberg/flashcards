from flask import Blueprint, request, jsonify
from sqlalchemy.sql.expression import func
from app.models import db, Card, Deck

card_bp = Blueprint('cards', __name__, url_prefix='/cards')

@card_bp.route('', methods=['GET'])
def get_cards():
    cards = Card.query.all()

    return jsonify([{
        "id": card.id,
        "front": card.front,
        "back": card.back,
        "deck_id": card.deck_id,
        "created_at": card.created_at,
        "updated_at": card.updated_at
    } for card in cards])

@card_bp.route('/<int:card_id>', methods=['GET'])
def get_card(card_id):
    card = Card.query.get_or_404(card_id)

    return jsonify({
        "id": card.id,
        "front": card.front,
        "back": card.back,
        "deck_id": card.deck_id,
        "created_at": card.created_at,
        "updated_at": card.updated_at
    })

@card_bp.route('', methods=['POST'])
def create_card():
    data = request.get_json()
    new_card = Card(front=data['front'], back=data['back'])
    db.session.add(new_card)
    db.session.commit()

    return jsonify({
        "id": new_card.id,
        "front": new_card.front,
        "back": new_card.back,
        "created_at": new_card.created_at,
        "updated_at": new_card.updated_at
    }), 201

@card_bp.route('/<int:card_id>', methods=['PATCH'])
def update_card(card_id):
    card = Card.query.get_or_404(card_id)
    data = request.get_json()

    allowed_fields = {'front', 'back', 'deck_id'}
    for field in allowed_fields:
        if field in data:
            if field == 'deck_id':
                if data['deck_id'] is None:
                    card.deck_id = None
                else:
                    deck = Deck.query.get(data['deck_id'])
                    if not deck:
                        return jsonify({"error": f"Deck with id {data['deck_id']} does not exist"}), 400
                    card.deck_id = data['deck_id']
            else:
                setattr(card, field, data[field])

    db.session.commit()


    return jsonify({
        "id": card.id,
        "front": card.front,
        "back": card.back,
        "deck_id": card.deck_id,
        "created_at": card.created_at,
        "updated_at": card.updated_at
    })

@card_bp.route('/<int:card_id>', methods=['DELETE'])
def delete_card(card_id):
    card = Card.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()

    return jsonify({"message": "Card deleted successfully"}), 200

@card_bp.route('/random/<int:deck_id>', methods=['GET'])
def get_random_card(deck_id):
    deck = Deck.query.get(deck_id)
    if not deck:
        return jsonify({"error": f"Deck with id {deck_id} does not exist"}), 404

    random_card = Card.query.filter_by(deck_id=deck_id).order_by(func.random()).first()

    if not random_card:
        return jsonify({"error": f"No cards available in deck with id {deck_id}"}), 404

    return jsonify({
    "id": random_card.id,
    "front": random_card.front,
    "back": random_card.back,
    "deck_id": random_card.deck_id
})
