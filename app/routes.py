from flask import render_template, flash, url_for, request, redirect
from flask_login import login_user, login_required, logout_user, current_user
from app import app
from app.models import User
from app.forms import RegisterForm, LoginForm

# TODO Define logform and regform as global variables


@app.route("/", methods=["GET", "POST"])
def home():
    regform = RegisterForm()
    logform = LoginForm()
    if current_user.is_authenticated:
        redirect(url_for('user_dashboard'))
    return render_template("home.html", regform=regform, logform=logform)


@app.route("/login", methods=["GET", "POST"])
def login():
    logform = LoginForm()
    if request.method == "GET":
        return redirect(url_for('home'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('user_dashboard'))
        if logform.validate_on_submit():
            user = User.query.filter_by(phone=logform.phone.data).first()
            if user is None or not user.check_password(logform.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=logform.remember.data)
            return redirect(url_for("user_dashboard"))

    return redirect(url_for('home'))


@app.route("/register", methods=["GET", "POST"])
def register():
    regform = RegisterForm()
    if request.method == 'GET':
        return redirect(url_for('home'))
    else:
        if regform.validate_on_submit():
            new = User(name=regform.name.data, phone=regform.phone.data, email=regform.email.data)
            User.set_password(regform.password.data)
            db.session.add(new)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        else:
            flash("Form didn't validate")
            return redirect(url_for('register'))


# TODO change user's url
@app.route("/user/dashboard", methods=["GET", "POST"])
@login_required
def user_dashboard():
    # if current_user.money is None:
    current_user.money = 0
    # Add Money feature
    if request.method == "POST":
        current_user.money += int(request.form.get("add"))
    # TODO Implement Pay/receive
    return render_template("user.html", name=current_user.name, money=current_user.money)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))