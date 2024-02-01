from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import json
import time

s: str


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = r"/upload"
app.config["MAX_CONTENT_LENGTH"] = 256 * 1024 * 1024 

def add_to_image_counter() -> None:
    data: dict = {}
    with open("data.json","r") as f:
        data = json.load(f)
    data["images"] += 1
    with open("data.json","w") as f:
        json.dump(data,f)

def get_number() -> int:
    data: dict = {}
    with open("data.json","r") as f:
        data = json.load(f)
    return int(data["images"])

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
        filename: str = f.filename
        f.save(path+fr"/{secure_filename(f.filename)}")
        size: float = round(os.path.getsize(path+fr"/{secure_filename(f.filename)}") / 1000000,4)
        data["username"] = request.args.get("username",None)
        username: str = data["username"]
        data["time_uploaded"] = round(time.time())
        time_uploaded: int = data["time_uploaded"]
        data["ip"] = request.environ.get('HTTP_X_FORWARDED_FOR',request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
        data["headers"] = list(request.headers)
            
        data["ip6"] = ip
        with open(path+fr"/{filename.split('.')[:-1][0]}.data.json","w") as f:
            json.dump(data,f,indent=2)
        add_to_image_counter()
        print(time_uploaded)    
        return render_template(f'success.html',
                               number=get_number(),
                               username=username,
                               time=time_uploaded,
                               filename=filename,
                               size=size
                            )

    return "Ignorind 'GET' request..."

@app.errorhandler(413)
def page_not_found(e):
    #print(e)
    #print(dir(e))
    #return render_template(...)
    return 'Your file is too big. The maximum size is 256mb.\n' + str(e)

app.run("192.168.100.45",80)