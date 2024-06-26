# cd /var/www/digithink
# git pull && mkdocs build -d stage
# rm -rf osite&&mv site osite&&mv stage site
# git pull && mkdocs build -d stage
# rm -rf osite&&mv site osite&&mv stage site

from flask import Flask
from markupsafe import escape
import subprocess

app = Flask(__name__)

@app.route("/whiskey/<style>",methods = ['POST', 'GET'])
def whiskey(style):
    ret=subprocess.call(['git', 'pull'], cwd="/var/www/digithink")
    ret=subprocess.call(['mkdocs', 'build'], cwd="/var/www/digithink")
    return f"One Whiskey, {escape(style)}!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')