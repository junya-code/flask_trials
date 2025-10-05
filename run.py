import webbrowser
from junya_flask import app
import os

if __name__ == "__main__":
    # 再起動プロセスじゃないときだけブラウザを開く
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)
