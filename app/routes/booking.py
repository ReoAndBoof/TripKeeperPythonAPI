# app/routes/booking.py

from flask import Blueprint, jsonify, request
from app.services.booking_service import search_booking_hotels

booking_bp = Blueprint("booking", __name__, url_prefix="/api/booking")


@booking_bp.route("/search", methods=["GET"])
def booking_search():
    """
    /api/booking/search?ss=Tokyo&checkin=2025-11-20&checkout=2025-11-22
    みたいに叩くと、Booking.com をスクレイピングして結果を返す。
    """
    
    ss = request.args.get("ss", "Tokyo")
    checkin = request.args.get("checkin")
    checkout = request.args.get("checkout")
    group_adults = int(request.args.get("group_adults", 2))
    group_children = int(request.args.get("group_children", 1))
    child_age = int(request.args.get("child_age", 10))
    currency = request.args.get("currency", "USD")

    if not checkin or not checkout:
        return jsonify({"error": "checkin and checkout are required"}), 400

    hotels = search_booking_hotels(
        ss=ss,
        checkin=checkin,
        checkout=checkout,
        group_adults=group_adults,
        group_children=group_children,
        child_age=child_age,
        currency=currency,
    )

    return jsonify({"count": len(hotels), "hotels": hotels})
