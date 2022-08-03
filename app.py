<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.cjl2gkt.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta
=======
from multiprocessing.sharedctypes import Value
from pymongo import MongoClient
import jwt
import datetime
import hashlib
import certifi
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

ca = certifi.where()
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = "./static/profile_pics"

SECRET_KEY = "chapter01"

client = MongoClient(
    "mongodb+srv://chapter01:chapter01@chapter01.lnhgc.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=ca,
)
db = client.chapter01


###########

#################################
##  HTML을 주는 부분##        ##
#################################
@app.route("/")
def home():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        return render_template("index.html", user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("register", msg="로그인 정보가 존재하지 않습니다."))


@app.route("/login")
def login():
    msg = request.args.get("msg")
    return render_template("login.html", msg=msg)


@app.route("/register")
def register():
    return render_template("register.html")


#################################
##  로그인을 위한 API          ##
#################################

# [아이디 중복확인]
@app.route("/register/check_dup", methods=["POST"])
def check_dup():
    username_receive = request.form["username_give"]
    exists = bool(db.user.find_one({"id": username_receive}))
    return jsonify({"result": "success", "exists": exists})


# [회원가입 API]
@app.route("/register/save", methods=["POST"])
def api_register():
    id_receive = request.form["id_give"]
    pw_receive = request.form["pw_give"]
    nickname_receive = request.form["nickname_give"]

    pw_hash = hashlib.sha256(pw_receive.encode("utf-8")).hexdigest()
    # pw2_hash = hashlib.sha256(pw2_receive.encode("utf-8")).hexdigest()

    doc = {"id": id_receive, "pw": pw_hash, "nick": nickname_receive}

    db.user.insert_one(doc)
    return jsonify({"result": "success"})


# [로그인]
@app.route("/login/sign_in", methods=["POST"])
def sign_in():
    # 로그인
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]

    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    result = db.user.find_one({"id": username_receive, "pw": pw_hash})

    if result is not None:
        payload = {
            "id": username_receive,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256").decode("utf-8")

        return jsonify({"result": "success", "token": token})
    # 찾지 못하면
    else:
        return jsonify({"result": "fail", "msg": "아이디/비밀번호가 일치하지 않습니다."})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
>>>>>>> bb4fe7436c7cb02acbd81cbc947fea4751b4dab8
