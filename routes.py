from app import app
from flask import render_template, request, redirect
import messages, users

@app.route("/")
def index():
    message_list = messages.get_list()
    return render_template("index.html", count=len(message_list), messages=message_list)


@app.route("/new")
def new():
    return render_template("new.html")


@app.route("/send", methods=["post"])
def send():
    content = request.form.get("content")

    if messages.send(content):
        return redirect("/")

    return render_template("error.html", message="Viestin lähetys ei onnistunut")


@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if users.login(username, password):
            return redirect("/")

        return render_template("error.html", message="Väärä tunnus tai salasana")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if users.register(username, password):
            return redirect("/")

        return render_template("error.html", message="Rekisteröinti ei onnistunut")
