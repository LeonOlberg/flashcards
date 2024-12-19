from flask import Blueprint, request, jsonify
from app.models import Card, Deck, db

api_bp = Blueprint('api', __name__)

@api_bp.route('/cards', methods=['GET'])
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

@api_bp.route('/cards/<int:card_id>', methods=['GET'])
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

@api_bp.route('/cards', methods=['POST'])
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

@api_bp.route('/cards/<int:card_id>', methods=['PATCH'])
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

@api_bp.route('/cards/<int:card_id>', methods=['DELETE'])
def delete_card(card_id):
    card = Card.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()

    return jsonify({"message": "Card deleted successfully"}), 200

@api_bp.route('/decks', methods=['GET'])
def get_decks():
    decks = Deck.query.all()

    return jsonify([{
        "id": deck.id,
        "title": deck.title,
        "category": deck.category,
        "created_at": deck.created_at,
        "updated_at": deck.updated_at
    } for deck in decks])

@api_bp.route('/decks', methods=['POST'])
def create_deck():
    data = request.get_json()
    new_deck = Deck(title=data['title'], category=data['category'])
    db.session.add(new_deck)
    db.session.commit()

    return jsonify({
        "id": new_deck.id,
        "title": new_deck.title,
        "category": new_deck.category,
        "created_at": new_deck.created_at,
        "updated_at": new_deck.updated_at
    }), 201