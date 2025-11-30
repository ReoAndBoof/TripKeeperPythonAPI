from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder="build")

# ルートアクセスで index.html を返す
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# build フォルダ内の他の静的ファイルを返す
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

# Render は PORT 環境変数を使用
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
