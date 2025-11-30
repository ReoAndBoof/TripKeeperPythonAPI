your-project/
├─ app/
│  ├─ main.py              ← FastAPI/Flask 本体
│  ├─ routes/
│  │   ├─ scraping.py      ← スクレイピングを叩くAPI or 画面
│  │   ├─ __init__.py
│  ├─ services/
│  │   ├─ scraping_service.py  ← スクレイピングのビジネスロジック
│  │   └─ __init__.py
│  ├─ scrapers/
│  │   ├─ base.py          ← 共通処理（ヘッダ設定・リトライなど）
│  │   ├─ example_site.py  ← 特定サイト用スクレイパー
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
