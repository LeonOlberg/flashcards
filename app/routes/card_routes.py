from flask import Blueprint, request, jsonify
from sqlalchemy.sql.expression import func
from app.models import db, Card, Deck, DrawnCard
from app.storage import storage_service
from werkzeug.utils import secure_filename

card_bp = Blueprint('cards', __name__, url_prefix='/cards')

def _get_card_response(card):
    """Helper function to format card response with presigned URLs."""
    return {
        "id": card.id,
        "front": card.front,
        "back": card.back,
        "front_img": storage_service.get_file_url(card.front_img) if card.front_img else None,
        "back_img": storage_service.get_file_url(card.back_img) if card.back_img else None,
        "deck_id": card.deck_id,
        "created_at": card.created_at,
        "updated_at": card.updated_at
    }

@card_bp.route('', methods=['GET'])
def get_cards():
    cards = Card.query.all()
    return jsonify([_get_card_response(card) for card in cards])

@card_bp.route('/<string:card_id>', methods=['GET'])
def get_card(card_id):
    card = Card.query.get_or_404(card_id)
    return jsonify(_get_card_response(card))

@card_bp.route('', methods=['POST'])
def create_card():
    data = request.form.to_dict()
    front_img = request.files.get('front_img')
    back_img = request.files.get('back_img')

    new_card = Card(
        front=data['front'],
        back=data['back']
    )

    if 'deck_id' in data and data['deck_id']:
        new_card.deck_id = data['deck_id']

    db.session.add(new_card)
    db.session.commit()

    # Upload images if provided
    if front_img:
        new_card.front_img = storage_service.upload_file(front_img, new_card.id, 'front')
    if back_img:
        new_card.back_img = storage_service.upload_file(back_img, new_card.id, 'back')

    db.session.commit()

    return jsonify(_get_card_response(new_card)), 201

@card_bp.route('/<string:card_id>', methods=['PATCH'])
def update_card(card_id):
    card = Card.query.get_or_404(card_id)
    data = request.form.to_dict()
    front_img = request.files.get('front_img')
    back_img = request.files.get('back_img')

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

    # Handle image uploads
    if front_img:
        card.front_img = storage_service.upload_file(front_img, card.id, 'front')
    if back_img:
        card.back_img = storage_service.upload_file(back_img, card.id, 'back')

    db.session.commit()

    return jsonify(_get_card_response(card))

@card_bp.route('/<string:card_id>', methods=['DELETE'])
def delete_card(card_id):
    card = Card.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()

    return jsonify({"message": "Card deleted successfully"}), 200

@card_bp.route('/random/<string:deck_id>', methods=['GET'])
def get_random_card(deck_id):
    deck = Deck.query.get(deck_id)
    if not deck:
        return jsonify({"error": f"Deck with id {deck_id} does not exist"}), 404

    # Get cards in the deck
    cards_in_deck = Card.query.filter_by(deck_id=deck_id).all()

    if not cards_in_deck:
        return jsonify({"error": f"No cards available in deck with id {deck_id}"}), 404

    # Check if we have drawn card records for this deck
    drawn_card_ids = db.session.query(DrawnCard.card_id).filter(
        DrawnCard.card_id.in_([card.id for card in cards_in_deck]),
        DrawnCard.is_drawn == True
    ).all()
    drawn_card_ids = [str(card_id[0]) for card_id in drawn_card_ids]

    # Filter cards that haven't been drawn yet
    undrawn_cards = [card for card in cards_in_deck if str(card.id) not in drawn_card_ids]

    if not undrawn_cards:
        return jsonify({"error": f"There are no more cards to be drawn in the Deck: {deck.title}"}), 404

    # Get a random card from undrawn cards
    import random
    random_card = random.choice(undrawn_cards)

    # Mark card as drawn
    drawn_card = DrawnCard.query.filter_by(card_id=random_card.id).first()
    if drawn_card:
        drawn_card.is_drawn = True
    else:
        drawn_card = DrawnCard(card_id=random_card.id, is_drawn=True)
        db.session.add(drawn_card)

    db.session.commit()

    return jsonify(_get_card_response(random_card))

@card_bp.route('/reset/<string:deck_id>', methods=['PUT'])
def reset_drawn_cards(deck_id):
    deck = Deck.query.get(deck_id)
    if not deck:
        return jsonify({"error": f"Deck with id {deck_id} does not exist"}), 404

    # Get all cards in the deck
    cards_in_deck = Card.query.filter_by(deck_id=deck_id).all()

    # Reset all drawn cards for this deck
    for card in cards_in_deck:
        drawn_card = DrawnCard.query.filter_by(card_id=card.id).first()
        if drawn_card:
            drawn_card.is_drawn = False
        else:
            drawn_card = DrawnCard(card_id=card.id, is_drawn=False)
            db.session.add(drawn_card)

    db.session.commit()

    return jsonify({"message": f"The Deck with id {deck_id} has been reset"}), 200
