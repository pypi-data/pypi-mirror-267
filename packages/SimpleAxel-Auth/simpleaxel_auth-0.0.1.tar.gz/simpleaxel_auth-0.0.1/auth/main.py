from flask import Blueprint, render_template, redirect, request, make_response
from simplesdk.internal import AlphacrmSDK, safe_hash, uuid4
from os import environ
from dotenv import load_dotenv
from datetime import datetime, timedelta
from random import randrange
from simplesdk.translations import translation, language

loc = translation(
    environ["ET_TRANSLATIONS"]
    or "https://git.tech.eus/EuskadiTech/Translations/raw/branch/main/SimpleAxel.json"
)

load_dotenv()

app = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")
client = AlphacrmSDK(environ["ET_USER"], environ["ET_PASSWORD"], environ["ET_BASEURL"])


def login_session():
    user = client.login_with_session(request.cookies.get("et_auth_session"))
    return user


@app.route("/login")
def login():
    return render_template(
        "auth/login.html", __=language(loc, request.cookies.get("lang") or "es")
    )


@app.route("/invalid")
def invalid():
    return render_template(
        "auth/invalid.html", __=language(loc, request.cookies.get("lang") or "es")
    )


@app.route("/invalid-signup")
def invalid_signup():
    return render_template(
        "auth/invalid-signup.html",
        __=language(loc, request.cookies.get("lang") or "es"),
    )


@app.route("/register")
def register():
    return render_template(
        "auth/register.html", __=language(loc, request.cookies.get("lang") or "es")
    )


@app.route("/_/login", methods=["POST"])
def api_login():
    data = client.login_with_combo(request.form["email"], request.form["password"])
    if data == None:
        return redirect("/auth/invalid")
    session = data["0(clientes)"]["session"]
    r = make_response(redirect("/account"))
    r.set_cookie(
        "et_auth_session",
        session,
        max_age=timedelta(weeks=7),
        expires=datetime.now() + timedelta(weeks=7),
    )
    return r


@app.route("/_/logout", methods=["POST", "GET"])
def api_logout():
    data = login_session()
    data["0(clientes)"]["session"] = uuid4().hex
    client.register(data)
    r = make_response(redirect("/account"))
    r.set_cookie("et_auth_session", "eee", expires=datetime.now() + timedelta(weeks=7))
    return redirect("/")


@app.route("/_/register", methods=["POST"])
def api_register():
    content = {
        "0(clientes)": {
            "id": randrange(31416, 9999999),
            "clave_hash": safe_hash(request.form["password"]),
            "correo": request.form["email"],
            "nombre": request.form["accname"] + "; [WEB]",
            "session": uuid4().hex,
        }
    }
    user = [
        u for u in client.users() if u["0(clientes)"]["correo"] == request.form["email"]
    ]
    if user != []:
        return redirect("/auth/invalid-signup")
    client.register(content)
    client.login_with_session(content["0(clientes)"]["session"])
    session = content["0(clientes)"]["session"]
    r = make_response(redirect("/account"))
    r.set_cookie("et_auth_session", session, expires=datetime.now() + timedelta(days=7))
    return r
