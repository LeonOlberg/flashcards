from app import create_app, db
from app.models import Card, Deck, DrawnCard, DeckCategory
from faker import Faker
import uuid

app = create_app()
fake = Faker()

with app.app_context():
    print('Seeding the database...')
    print('Dropping and recreating all tables...')
    db.drop_all()
    db.create_all()

    categories = list(DeckCategory)
    decks = []

    print('Adding decks...')
    #Generate some random decks
    for _ in range(5):
        deck = Deck(title=fake.sentence(nb_words=2), category=fake.random_element(categories))
        decks.append(deck)

    db.session.add_all(decks)
    db.session.commit()

    print('Adding cards...')
    #Generate some random cards for each deck
    for deck in decks:
        cards = []
        drawn_cards = []
        for _ in range(10):
            card = Card(id=uuid.uuid4(), front=fake.sentence(nb_words=5), back=fake.sentence(nb_words=10), deck_id=deck.id)
            drawn_card = DrawnCard(card_id=card.id, is_drawn=False)

            cards.append(card)
            drawn_cards.append(drawn_card)

        db.session.add_all(cards)
        db.session.add_all(drawn_cards)
    db.session.commit()

    print('Database successfully seeded with random data!!')
