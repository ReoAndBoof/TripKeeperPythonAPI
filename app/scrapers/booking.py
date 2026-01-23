# app/scrapers/booking.py

from playwright.sync_api import sync_playwright
import random
import threading
import atexit

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.140 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.140 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36",
]

VIEWPORTS = [
    {"width": 1280, "height": 800},
    {"width": 1366, "height": 768},
    {"width": 1440, "height": 900},
    {"width": 1920, "height": 1080},
]

# ---- 常駐 Playwright / Browser ----
_pw = None
_browser = None
_lock = threading.Lock()   # 同時アクセス保護（Wixから並列で来る可能性があるため）

def _ensure_browser():
    """
    プロセス内で Playwright と Browser を1回だけ起動して使い回す。
    """
    global _pw, _browser
    if _browser is not None:
        return _browser

    with _lock:
        if _browser is not None:
            return _browser

        _pw = sync_playwright().start()
        _browser = _pw.chromium.launch(
            headless=True,
            args=[
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
            ],
        )
        return _browser

def _shutdown():
    global _pw, _browser
    try:
        if _browser is not None:
            _browser.close()
    finally:
        _browser = None
        try:
            if _pw is not None:
                _pw.stop()
        finally:
            _pw = None

atexit.register(_shutdown)

# ---- スクレイプ本体 ----
def scrape_booking(url: str, max_scrolls: int = 0) -> list[dict]:
    """
    Booking.com 検索結果から name / price / url を取得（高速版）
    max_scrolls: 無限スクロールで追加ロードが必要なときだけ >0 にする
    """
    browser = _ensure_browser()
    ua = random.choice(USER_AGENTS)
    vp = random.choice(VIEWPORTS)

    # ※ context/page は毎回作って毎回閉じる（これが安全＆速い）
    context = browser.new_context(
        user_agent=ua,
        viewport=vp,
        locale="en-US",
        timezone_id="Asia/Tokyo",
    )
    page = context.new_page()

    try:
        # 重いリソースをブロック（さらに攻めるなら stylesheet も切れる）
        def block_resources(route):
            r = route.request
            if r.resource_type in {"image", "media", "font"}:
                return route.abort()
            if any(x in r.url for x in ["doubleclick", "googletagmanager", "google-analytics"]):
                return route.abort()
            return route.continue_()

        page.route("**/*", block_resources)

        # domcontentloaded すら待たず commit → selector で止める方が速いことが多い
        page.goto(url, wait_until="commit", timeout=20000)

        page.wait_for_selector(
            "div[data-testid='property-card'][role='listitem']",
            timeout=20000
        )

        for _ in range(max_scrolls):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(600)

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
        return hotels

    finally:
        # browser は閉じない（常駐）
        context.close()
