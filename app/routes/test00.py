
# app/routes/test00.py

from flask import Blueprint, jsonify, request
from app.services.booking_service import search_booking_hotels

test00_bp = Blueprint("test00", __name__)


@test00_bp.route("/api/booking/search", methods=["GET"])
def booking_search():
    """
    /api/booking/search?city=Tokyo&checkin=2025-11-20&checkout=2025-11-22
    みたいに叩くと、Booking.com をスクレイピングして結果を返す。
    """
    
    city = request.args.get("city", "Tokyo")
    checkin = request.args.get("checkin")
    checkout = request.args.get("checkout")
    adults = int(request.args.get("adults", 2))
    children = int(request.args.get("children", 1))
    child_age = int(request.args.get("child_age", 10))
    currency = request.args.get("currency", "USD")

    if not checkin or not checkout:
        return jsonify({"error": "checkin and checkout are required"}), 400

    hotels = search_booking_hotels(
        city=city,
        checkin=checkin,
        checkout=checkout,
        adults=adults,
        children=children,
        child_age=child_age,
        currency=currency,
    )

    return jsonify({"count": len(hotels), "hotels": hotels})
