
from flask import Flask
from markupsafe import escape
import subprocess

app = Flask(__name__)

@app.route("/whiskey/<style>",methods = ['POST', 'GET'])
def whiskey(style):
    # break this out by style.
    subprocess.call(['at', 'now', '-f', '/var/www/digithink/whiskey/pullandbuild.sh'])
# subprocess.call(['mkdocs', 'build'], cwd="/var/www/digithink")
    return f"One Whiskey, {escape(style)}!"

@app.route("/")
def root():
    return f"Not much here...."

if __name__ == "__main__":
    app.run(host='0.0.0.0')