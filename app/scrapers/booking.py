# app/scrapers/booking.py

from playwright.sync_api import sync_playwright
import time
import random

"""
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


def scrape_booking(url: str, max_scrolls: int = 0) -> list[dict]:
    """
    Booking.com 検索結果から name / price / url を取得（高速版）
    max_scrolls: 無限スクロールで追加ロードが必要なときだけ >0 にする
    """
    def _run(playwright):
        ua = random.choice(USER_AGENTS)
        vp = random.choice(VIEWPORTS)

        browser = playwright.chromium.launch(
            headless=True,
            args=[
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
            ],
        )

        context = browser.new_context(
            user_agent=ua,
            viewport=vp,
            locale="en-US",
        )

        page = context.new_page()

        # 1) 重いリソースをブロックして高速化
        def block_resources(route):
            r = route.request
            if r.resource_type in {"image", "media", "font"}:
                return route.abort()
            # tracking系を雑に切る（必要なら調整）
            if any(x in r.url for x in ["doubleclick", "googletagmanager", "google-analytics"]):
                return route.abort()
            return route.continue_()

        page.route("**/*", block_resources)

        # 2) ナビゲーションは必要最低限待つ（domcontentloadedでOK）
        page.goto(url, wait_until="domcontentloaded", timeout=20000)

        # 3) カードが出たらすぐ進む
        page.wait_for_selector("div[data-testid='property-card']", timeout=30000)

        # 4) 追加ロードが必要なときだけスクロール（最小回数）
        #    まずは max_scrolls=0 で試すのがおすすめ
        for _ in range(max_scrolls):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(600)  # 小さめ

        # 5) DOM抽出は evaluate で一括（ここが効く）
        hotels = page.evaluate(
            """
            () => {
              const cards = Array.from(document.querySelectorAll("div[data-testid='property-card'][role='listitem']"));
              return cards.map(card => {
                const nameEl = card.querySelector("div[data-testid='title']");
                const priceEl = card.querySelector("span[data-testid='price-and-discounted-price']");
                const linkEl = card.querySelector("a[data-testid='title-link']");
                const name = nameEl ? nameEl.textContent.trim() : null;
                const price = priceEl ? priceEl.textContent.trim() : null;
                const url = linkEl ? linkEl.href : null;
                if (!name || !price || !url) return null;
                return { name, price, url };
              }).filter(Boolean);
            }
            """
        )

        context.close()
        browser.close()
        return hotels

    with sync_playwright() as p:
        return _run(p)
