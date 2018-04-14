from flask import Flask, render_template, url_for, request, session, redirect
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return render_template("user.html", name=request.form.get("username"))
    else:
        return render_template("home.html")


# TODO change user's url
@app.route("/user/", methods=["GET", "POST"])
def user():
    if session.get("money") is None:
        session["money"] = 0
    if request.method == "POST":
        add_money = int(request.form.get("add"))
        session["money"] += add_money
    return render_template("user.html", money=session["money"])


if __name__ == '__main__':
    app.run(debug=True)
