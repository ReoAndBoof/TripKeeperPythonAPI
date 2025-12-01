from flask import Flask, send_from_directory
import os

# プロジェクトルートを基準に build ディレクトリの絶対パスを作る
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_DIR = os.path.join(BASE_DIR, "build")
print(BUILD_DIR)
app = Flask(__name__, static_folder=BUILD_DIR)

# ルートアクセスで index.html を返す
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "API_index.html")

# build フォルダ内の他の静的ファイルを返す
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

# ★ ここで blueprint を登録
register_routes(app)

# Render は PORT 環境変数を使用
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
