from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/user/<username>")
def userpage(username):
    return render_template("user.html", name=username)


if __name__ == '__main__':
    app.run(debug=True)
