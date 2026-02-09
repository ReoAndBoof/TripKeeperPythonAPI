# app/services/booking_service.py

from urllib.parse import urlencode
from app.scrapers.booking import scrape_booking

BASE_URL = "https://www.booking.com/searchresults.html"


def build_booking_url(
    dest_id: str = "316", #shinjuku ward
    dest_type: str = "district", #範囲をせばめる
    ss: str = "Tokyo",
    checkin: str = "2025-11-20",
    checkout: str = "2025-11-22",
    group_adults: int = 2,
    group_children: int = 1,
    children_age: int = 10,
    no_rooms: int = 1,
    currency: str = "USD",
    nflt: str = "review_score%3D80%3B",
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
        "nflt": nflt,
        "order" : "popularity",
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
    nflt: str = "review_score%3D80%3Bprice%3DUSD-min-200-1",
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
        nflt=nflt,
        filters={
            # 例: 「朝食付き」など filter を追加したい場合
            # "nflt": "fc=2",
        },
    )
    #url = 'https://www.booking.com/searchresults.html?offset=0&label=keio-plaza-tokyo-y041XbvRkrnVnbUH_q2zbwS162174451113%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-56026848433%3Alp9030951%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YcUSe6BbHz0A_uhMSOKgInk&sid=8fc8adfb982b4a7eb5e2de9114e92553&aid=311088&ss=Shinjuku+Ward%2C+Tokyo%2C+Tokyo-to%2C+Japan&ssne=Shibuya+Ward&ssne_untouched=Shibuya+Ward&highlighted_hotels=179845&lang=en-us&src=searchresults&dest_id=316&dest_type=district&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=4&search_selected=true&search_pageview_id=1e263caa94fcf10cd0581cb5c4086b01&checkin=2026-02-18&checkout=2026-02-19&group_adults=2&no_rooms=1&group_children=0&nflt=review_score%3D80%3Bfc%3D2%3Bht_id%3D204%3Bht_id%3D209'
    print(url)
    hotels = scrape_booking(url, 0)
    return hotels
