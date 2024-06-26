from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route("/whiskey/<style>")
def whiskey(style):
    return f"One Whiskey, {escape(style)}!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')