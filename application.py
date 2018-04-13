from flask import Flask, render_template, redirect, flash, url_for
# from flask_login import current_user, login_user
from forms import LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


@app.route("/", methods=['GET', 'POST'])
def main():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect('/user/')
    return render_template('index.html', form=form)


@app.route("/user/<username>")
def userpage(username):
    return render_template("user.html", name=username)


if __name__ == '__main__':
    app.run(debug=True)
