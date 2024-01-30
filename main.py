from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import json
import time
s: str


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = r"/upload"
app.config["MAX_CONTENT_LENGTH"] = 256 * 1024 * 1024 

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/endpoint", methods=["POST","GET"])
def endpoint():

    if request.method == "POST":
        data: dict = {}
        ip: str = request.remote_addr
        path: str = os.getcwd() + os.path.join(app.config['UPLOAD_FOLDER'], ip)
        os.makedirs(path,exist_ok=True)
        
        f = request.files["file"]
        f.save(path+fr"/{secure_filename(f.filename)}")
        
        data["username"] = request.args.get("username",None)
        data["time_uploaded"] = round(time.time())
        data["ip"] = request.environ.get('HTTP_X_FORWARDED_FOR',request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
        data["headers"] = list(request.headers)

        data["ip6"] = ip
        with open(path+r"/data.json","w") as f:
            json.dump(data,f,indent=2)
        return render_template("success.html")

    return "Ignorind 'GET' request..."

app.run("192.168.100.45",5000)