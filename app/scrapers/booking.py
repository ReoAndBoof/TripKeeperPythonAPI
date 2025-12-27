# app/scrapers/booking.py

from playwright.sync_api import sync_playwright
import time
import random

def human_delay(min_sec=0.5, max_sec=2):
    time.sleep(random.uniform(min_sec, max_sec))
""""
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.140 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36",
]
"""
USER_AGENTS = [
    # Chrome Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.140 Safari/537.36",
    # Chrome macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.140 Safari/537.36",
    # Chrome Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36",
]

VIEWPORTS = [
    {"width": 1280, "height": 800},
    {"width": 1366, "height": 768},
    {"width": 1440, "height": 900},
    {"width": 1920, "height": 1080},
]


def scrape_booking(url: str) -> list[dict]:
    """
    指定された Booking.com の検索結果URLから
    ホテルの name / price / url をリストで返す。
    """

    def _run(playwright):
        ua = random.choice(USER_AGENTS)
        vp = random.choice(VIEWPORTS)

        browser = playwright.chromium.launch(headless=True, slow_mo=0)
        page = browser.new_page(
            user_agent=ua,
            viewport=vp,
            locale="en-US",
        )

        print("Access url:", url)
        page.goto(url, wait_until="domcontentloaded")

        # 検索結果のカードが表示されるまで待機
        page.wait_for_selector("div[data-testid='property-card']", timeout=30000)
        print("ホテルリスト検出 ✅")

        # 必要なら少し待つ
        # human_delay(1, 3)

        hotel_cards = page.query_selector_all(
            "div[data-testid='property-card'][role='listitem']"
        )
        print(f"ホテル件数: {len(hotel_cards)}")

        hotels: list[dict] = []

        for card in hotel_cards:
            try:
                name_el = card.query_selector("div[data-testid='title']")
                price_el = card.query_selector(
                    "span[data-testid='price-and-discounted-price']"
                )
                link_el = card.query_selector("a[data-testid='title-link']")

                if not (name_el and price_el and link_el):
                    continue

                name = name_el.inner_text().strip()
                print(name)
                price_total = price_el.inner_text().strip()
                print(price_total)
                link = link_el.get_attribute("href")
                print(link)

                hotels.append(
                    {
                        "name": name,
                        "price": price_total,
                        "url": link,
                    }
                )
            except Exception as e:
                print("Error parsing card:", e)

        browser.close()
        print("scraping ok")
        return hotels

    with sync_playwright() as p:
        return _run(p)
