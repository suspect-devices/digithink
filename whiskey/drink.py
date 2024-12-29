# Bare Bones POC 
#  Signature code stolen directly from Lukas Pühringer 
#     https://gist.github.com/lukpueh/498ff3489321bdc7106c05a2fd5b941c
#     NOTE: Rquires payload to be set to json
#  https://blog.gitguardian.com/how-to-handle-secrets-in-python/
from flask import Flask , request, abort
from markupsafe import escape
from dotenv import load_dotenv
import hmac
import hashlib
import os
import subprocess

app = Flask(__name__)

load_dotenv()
GITHUB_SECRET = os.getenv("GITHUB_SECRET")

@app.route("/whiskey/<style>",methods = ['POST', 'GET'])
def whiskey(style):
  
  # Extract signature header
  signature = request.headers.get("X-Hub-Signature")
  if not signature or not signature.startswith("sha1="):
    abort(400, "X-Hub-Signature required")

  # Create local hash of payload
  digest = hmac.new(GITHUB_SECRET.encode(),
      request.data, hashlib.sha1).hexdigest()

  # Verify signature
  if not hmac.compare_digest(signature, "sha1=" + digest):
    #abort(400, signature+"<>sha1="+digest)
    abort(400, "I am going to need to see some id.")

  # After we have detemined that this is legit.
  match style:
    case "neat":
      subprocess.call(['at', 'now', '-f', '/var/www/digithink/whiskey/pullandbuild.sh'])
    case "sour":
      subprocess.call(['at', 'now', '-f', '/var/www/3dangst/repo/makesite.sh'])
    case _: abort(404,"We Don't Serve That Here!")
    
  return f"One Whiskey, {escape(style)}!"

@app.route("/")
def root():
    return f"Not much here...."

if __name__ == "__main__":
    app.run(host='0.0.0.0')
