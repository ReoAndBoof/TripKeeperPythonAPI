# app/services/test00_service.py

from urllib.parse import urlencode
from app.scrapers.test00 import scrape_test00

BASE_URL = "https://www.booking.com/searchresults.html"


def build_booking_url(
    dest_id: str = "-246227",
    dest_type: str = "city",
    ss: str = "Tokyo",
    checkin: str = "2025-11-20",
    checkout: str = "2025-11-22",
    group_adults: int = 2,
    group_children: int = 1,
    children_age: int = 10,
    no_rooms: int = 1,
    currency: str = "USD",
    filters: dict | None = None,
) -> str:
    """
    Booking.com 検索URLを組み立てる。
    ※ パラメータは必要に応じて増やしてOK
    """

    params = {
        "ss": ss,
        "lang": "en-us",
        "src": "searchresults",
        "dest_id": dest_id,
        "dest_type": dest_type,
        "checkin": checkin,
        "checkout": checkout,
        "group_adults": group_adults,
        "no_rooms": no_rooms,
        "group_children": group_children,
        "age": children_age,
        "selected_currency": currency,
    }

    if filters:
        params.update(filters)

    return f"{BASE_URL}?{urlencode(params)}"


def search_booking_hotels(
    ss: str,
    checkin: str,
    checkout: str,
    group_adults: int = 2,
    group_children: int = 1,
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
        ss=ss,
        checkin=checkin,
        checkout=checkout,
        group_adults=group_adults,
        group_children=group_children,
        children_age=child_age,
        currency=currency,
        filters={
            # 例: 「朝食付き」など filter を追加したい場合
            # "nflt": "fc=2",
        },
    )

    hotels = scrape_booking(url)
    return hotels
