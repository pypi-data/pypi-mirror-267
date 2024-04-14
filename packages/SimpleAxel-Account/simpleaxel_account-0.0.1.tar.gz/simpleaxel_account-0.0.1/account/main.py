from flask import Blueprint, render_template, redirect, request
from simplesdk.internal import AlphacrmSDK, AulaSDK
from os import environ
from dotenv import load_dotenv
from simplesdk.translations import translation, language

loc = translation(
    environ["ET_TRANSLATIONS"]
    or "https://git.tech.eus/EuskadiTech/Translations/raw/branch/main/SimpleAxel.json"
)

load_dotenv()

app = Blueprint("account", __name__, url_prefix="/account", template_folder="templates")
client = AlphacrmSDK(environ["ET_USER"], environ["ET_PASSWORD"], environ["ET_BASEURL"])
client2 = AulaSDK(environ["ET_USER"], environ["ET_PASSWORD"], environ["ET_BASEURL"])


def login_session():
    user = client.login_with_session(request.cookies.get("et_auth_session"))
    return user


@app.route("/")
def index():
    user = login_session()
    if user == None:
        return redirect("/auth/login")
    a = [
        aula
        for aula in client2.aulas__all()
        if aula["1(clientes)"]["correo"] == user["0(clientes)"]["correo"]
    ]
    return render_template(
        "account/index.html",
        user=user["0(clientes)"],
        products=str(user["0(clientes)"]["products"]).split(),
        aulas=a,
        __=language(loc, request.cookies.get("lang") or "es"),
    )


@app.route("/buy_aula7")
def buy_aula7():
    user = login_session()
    if user == None:
        return redirect("/auth/login")
    return render_template(
        "account/buy_aula7.html",
        user=user["0(clientes)"],
        __=language(loc, request.cookies.get("lang") or "es"),
    )
