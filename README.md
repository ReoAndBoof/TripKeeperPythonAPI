your-project/
├─ app/
│  ├─ main.py                 ← Flask 本体（静的配信 + ルーティング登録）
│  ├─ routes/
│  │   ├─ booking.py          ← Booking.com 検索API　HTTPルート（APIの入口）
│  │   └─ __init__.py
│  ├─ services/
│  │   ├─ booking_service.py  ← Booking.com 用サービス層、スクレイピングをまとめたり、DB 保存・整形などをやる「サービス」層
│  │   └─ __init__.py
│  ├─ scrapers/
│  │   ├─ booking.py          ← Playwright で実際にスクレイプする層　外部APIみたいに扱うイメージ
│  │   └─ __init__.py
│  ├─ utils/
│  │   ├─ logger.py
│  │   └─ __init__.py
│  └─ __init__.py
│
├─ requirements.txt
├─ render.yaml             ← （任意）Render 自動設定
├─ .gitignore
├─ main.py                 ← Render エントリ用
└─ README.md

routes …「HTTPの入口」（Flask的にはルート／コントローラ）
services …「こういう条件でホテル検索して、必要なら整形も保存もする層」
scrapers …「Playwrightを叩いて、HTMLをパースして、Pythonのデータにする層」
utils …「どこからでも使いたい共通関数（ログなど）」
app/main.py & ルート main.py …「アプリの起動とルーティング登録」

ブラウザ/Wix/
        │
        ▼
【① HTTP リクエスト】
GET /api/booking/search?city=Tokyo&checkin=2025-11-20&checkout=2025-11-22
        │
        ▼
app/main.py（Flask アプリ本体）
        │
        ▼
app/routes/booking.py（ルート＝コントローラ）
        │
        ▼
app/services/booking_service.py（ビジネスロジック）
        │
        ▼
app/scrapers/booking.py（Playwrightスクレイパー）
        │
        ▼
Booking.com（外部サイト）
        │
        ▼
【ホテル情報のJSON取得】
        │
        ▼
ブラウザに JSON レスポンスが返る
