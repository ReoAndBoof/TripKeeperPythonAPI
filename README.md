your-project/
├─ app/
│  ├─ main.py              ← FastAPI/Flask 本体
│  ├─ routes/
│  │   ├─ wix.py           ← Wix callbacks / API routes
│  │   ├─ stripe.py        ← Stripe setup-intent / webhook
│  │   └─ __init__.py
│  ├─ services/
│  │   ├─ wix_service.py   ← Wix SDK or OAuth refresh logic
│  │   ├─ stripe_service.py← Stripe API wrapper
│  │   └─ __init__.py
│  ├─ utils/
│  │   ├─ logger.py        ← ログ設定
│  │   └─ __init__.py
│  └─ __init__.py
│
├─ requirements.txt
├─ render.yaml             ← （任意）Render 自動設定
├─ .gitignore
└─ README.md
