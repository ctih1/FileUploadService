from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import json
import time
app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = r"\upload"
app.config["MAX_CONTENT_LENGTH"] = 256 * 1024 * 1024 

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/endpoint", methods=["POST","GET"])
def endpoint():
    data: dict = {}
    if request.method == "POST":
        ip: str = request.remote_addr
        path: str = os.getcwd() + os.path.join(app.config['UPLOAD_FOLDER'], ip)
        os.makedirs(path,exist_ok=True)
        f = request.files["file"]
        f.save(path+fr"\{secure_filename(f.filename)}")
        data["username"] = request.args.get("username",None)
        data["time_uploaded"] = round(time.time())
        data["ip1"] =  request.environ['REMOTE_ADDR']
        data["ip2"] = request.remote_addr
        data["ip3"] = request.environ.get('HTTP_X_FORWARDED_FOR',None)
        data["ip4"] = request.environ.get('HTTP_X_REAL_IP', None)   
        data["ip5"] = request.access_route
        data["headers"] = list(request.headers)
        if not request.headers.getlist("X-Forwarded-For"):
            ip = request.remote_addr
        else:
            ip = request.headers.getlist("X-Forwarded-For")[0]
        data["ip6"] = ip
        with open(path+r"\data.json","w") as f:
            json.dump(data,f,indent=2)
        return "Saved!"
    return "Ignorind 'GET' request..."
app.run("192.168.100.32",5000)