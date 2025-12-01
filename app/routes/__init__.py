# app/routes/__init__.py

from .booking import booking_bp

def register_routes(app):
    app.register_blueprint(booking_bp)
