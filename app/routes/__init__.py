from .card_routes import card_bp
from .deck_routes import deck_bp

def register_routes(app):
    app.register_blueprint(card_bp)
    app.register_blueprint(deck_bp)
