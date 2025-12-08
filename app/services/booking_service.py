# app/services/booking_service.py

from urllib.parse import urlencode
from app.scrapers.booking import scrape_booking

BASE_URL = "https://www.booking.com/searchresults.html"


def build_booking_url(
    dest_id: str = "-246227",
    dest_type: str = "city",
    city: str = "Tokyo",
    checkin: str = "2025-11-20",
    checkout: str = "2025-11-22",
    adults: int = 2,
    children: int = 1,
    children_age: int = 10,
    rooms: int = 1,
    currency: str = "USD",
    filters: dict | None = None,
) -> str:
    """
    Booking.com 検索URLを組み立てる。
    ※ パラメータは必要に応じて増やしてOK
    """

    params = {
        "ss": city,
        "lang": "en-us",
        "src": "searchresults",
        "dest_id": dest_id,
        "dest_type": dest_type,
        "checkin": checkin,
        "checkout": checkout,
        "group_adults": adults,
        "no_rooms": rooms,
        "group_children": children,
        "age": children_age,
        "selected_currency": currency,
    }

    if filters:
        params.update(filters)

    return f"{BASE_URL}?{urlencode(params)}"


def search_booking_hotels(
    city: str,
    checkin: str,
    checkout: str,
    adults: int = 2,
    children: int = 1,
    child_age: int = 10,
    currency: str = "USD",
) -> list[dict]:
    """
    Booking.com からホテル一覧を取得するサービス関数。
    ルートからはこの関数だけを呼べばOK。
    """
    """
    とりあえずダミーデータを返す実装。
    /api/booking/search が 200 で返るかの疎通確認用。
    """
    """
    dummy_hotels = [
        {
            "name": f"Dummy Hotel 1 in {city}",
            "price": "USD 100",
            "url": "https://example.com/hotel1",
        },
        {
            "name": f"Dummy Hotel 2 in {city}",
            "price": "USD 150",
            "url": "https://example.com/hotel2",
        },
        {
            "name": f"Dummy Hotel 3 in {city}",
            "price": "USD 180",
            "url": "https://example.com/hotel3",
        },

    ]

    return dummy_hotels
    """

    url = build_booking_url(
        city=city,
        checkin=checkin,
        checkout=checkout,
        adults=adults,
        children=children,
        children_age=child_age,
        currency=currency,
        filters={
            # 例: 「朝食付き」など filter を追加したい場合
            # "nflt": "fc=2",
        },
    )

    hotels = scrape_booking(url)
    return hotels
