# app/routes/__init__.py

from .booking import booking_bp
from .test00 import test00_bp

def register_routes(app):
    app.register_blueprint(booking_bp)
    app.register_blueprint(test00_bp)
