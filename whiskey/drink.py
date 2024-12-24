# Bare Bones POC Needs to at least check the github secret
from flask import Flask
from markupsafe import escape
import subprocess

app = Flask(__name__)

@app.route("/whiskey/<style>",methods = ['POST', 'GET'])
def whiskey(style):
    # break this out by style.
    match style:
      case "neat":
        subprocess.call(['at', 'now', '-f', '/var/www/digithink/whiskey/pullandbuild.sh'])
      case "sour":
        subprocess.call(['at', 'now', '-f', '/var/www/3dangst/repo/makesite.sh'])
    return f"One Whiskey, {escape(style)}!"

@app.route("/")
def root():
    return f"Not much here...."

if __name__ == "__main__":
    app.run(host='0.0.0.0')
