# app/scrapers/booking.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional
import random

from playwright.sync_api import sync_playwright, Playwright


DEFAULT_USER_AGENTS = [
    # Chrome Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.140 Safari/537.36",
    # Chrome macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.140 Safari/537.36",
    # Chrome Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36",
]

DEFAULT_VIEWPORTS = [
    {"width": 1280, "height": 800},
    {"width": 1366, "height": 768},
    {"width": 1440, "height": 900},
    {"width": 1920, "height": 1080},
]


@dataclass
class BookingScraper:
    headless: bool = True
    locale: str = "en-US"
    timeout_goto_ms: int = 20_000
    timeout_cards_ms: int = 30_000
    scroll_wait_ms: int = 600

    user_agents: list[str] = field(default_factory=lambda: DEFAULT_USER_AGENTS.copy())
    viewports: list[dict] = field(default_factory=lambda: DEFAULT_VIEWPORTS.copy())

    block_resource_types: set[str] = field(default_factory=lambda: {"image", "media", "font"})
    block_url_keywords: tuple[str, ...] = ("doubleclick", "googletagmanager", "google-analytics")

    chromium_args: list[str] = field(
        default_factory=lambda: [
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled",
        ]
    )

    def _pick_ua_viewport(self) -> tuple[str, dict]:
        ua = random.choice(self.user_agents)
        vp = random.choice(self.viewports)
        return ua, vp

    def _route_handler(self, route):
        r = route.request
        if r.resource_type in self.block_resource_types:
            return route.abort()
        if any(k in r.url for k in self.block_url_keywords):
            return route.abort()
        return route.continue_()

    def scrape(self, url: str, max_scrolls: int = 0) -> list[dict]:
        """
        Booking.com 検索結果から name を取得（必要ならここを price/url 等に拡張）
        """
        def _run(pw: Playwright) -> list[dict]:
            ua, vp = self._pick_ua_viewport()

            browser = pw.chromium.launch(
                headless=self.headless,
                args=self.chromium_args,
            )
            context = browser.new_context(
                user_agent=ua,
                viewport=vp,
                locale=self.locale,
            )
            page = context.new_page()
            page.route("**/*", self._route_handler)

            page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_goto_ms)
            page.wait_for_selector("div[data-testid='property-card']", timeout=self.timeout_cards_ms)

            for _ in range(max_scrolls):
                page.mouse.wheel(0, 3000)
                page.wait_for_timeout(self.scroll_wait_ms)

            hotels = page.evaluate(
            """
            () => {
              const cards = Array.from(document.querySelectorAll("div[data-testid='property-card'][role='listitem']"));
              return cards.map(card => {
                const nameEl = card.querySelector("div[data-testid='title']");
                const priceEl = card.querySelector("span[data-testid='price-and-discounted-price']");
                // ロケーション（UI差分があるので候補を順に探す）
                const locationEl =
                    card.querySelector('[data-testid="address"]') ||
                    card.querySelector('[data-testid="location"]') ||
                    card.querySelector('[data-testid="address-link"]') ||
                    card.querySelector("span[class*='address']");
                const linkEl = card.querySelector("a[data-testid='title-link']");

                const name = nameEl ? nameEl.textContent.trim() : null;
                const price = priceEl ? priceEl.textContent.trim() : null;
                const location = locationEl ? locationEl.textContent.trim() : null;
                const url = linkEl ? linkEl.href : null;
                if (!name || !price || !url) return null;
                return { name, price, location, url };
              }).filter(Boolean);
            }
            """
            )

            context.close()
            browser.close()
            return hotels

        with sync_playwright() as pw:
            return _run(pw)

        
def filter_by_location(
    hotels: list[dict],
    keywords: list[str],
    field_name: str,
) -> list[dict]:
    normalized_keywords = [k.lower() for k in keywords]
    filtered = []
    for h in hotels:
        text = (h.get(field_name) or "")
        text_lower = text.lower()
        if any(k in text_lower for k in normalized_keywords):
            filtered.append(h)
    return filtered

# 既存の関数APIを残したいならラッパーも置ける
def scrape_booking(url: str, max_scrolls: int = 0) -> list[dict]:
    return BookingScraper().scrape(url, max_scrolls=max_scrolls)
