
from flask import Flask
from markupsafe import escape
import subprocess

app = Flask(__name__)

@app.route("/whiskey/<style>",methods = ['POST', 'GET'])
def whiskey(style):
    subprocess.call(['at', 'now', '-f', '/var/www/digithink/whiskey/pullandbuild.sh'])
# subprocess.call(['mkdocs', 'build'], cwd="/var/www/digithink")
    return f"One Whiskey, {escape(style)}!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')