from flask import render_template, flash, url_for, request, redirect
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import or_
from app import app, db
from app.models import User, Transactions
from app.forms import RegisterForm, LoginForm, TransactForm, SearchFilterForm


@app.route("/")
def home():
    regform = RegisterForm()
    logform = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))
    else:
        return render_template('home.html', regform=regform, logform=logform)


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
            login_user(user, remember=logform.remember_me.data)
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
            if regform.type.data == 'personal':
                new.type = 0
            elif regform.type.data == 'business':
                new.type = 1
            new.set_password(regform.password.data)
            db.session.add(new)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        else:
            flash("Form didn't validate")
            return redirect(url_for('register'))


# TODO change user's url
# TODO user can still go to the login page using browser back button
@app.route("/user/dashboard", methods=["GET", "POST"])
@login_required
def user_dashboard():
    transactform = TransactForm()
    TransactQuery = Transactions.query.join(User, (Transactions.payer_id == User.id)).filter(or_(Transactions.payer_id == current_user.id, Transactions.payee_id == current_user.id)).order_by(Transactions.timestamp.desc())
    # Add Money feature
    if request.method == "POST" and transactform.addbutton.data:
        current_user.money += int(transactform.add.data)
        db.session.commit()
        return redirect(url_for('user_dashboard'))
    if request.method == "POST" and transactform.paybutton.data:
        current_user.money -= int(transactform.pay.data)
        payee = User.query.filter_by(phone=transactform.payee.data).first()
        payee.money += int(transactform.pay.data)
        transact = Transactions(payer_id=current_user.id, payee_id=payee.id, amount=int(transactform.pay.data))
        db.session.add(transact)
        db.session.commit()
        return redirect(url_for('user_dashboard'))
    if request.method == 'POST' and request.form['filter'] == 'string':
        TransactQuery = Transactions.query.join(User, (Transactions.payer_id == User.id)).filter(or_(Transactions.payer_id == current_user.id, Transactions.payee_id == current_user.id)).filter(Transactions.timestamp.between(request.form.get('from'), request.form.get('to'))).order_by(Transactions.timestamp.desc())
    if request.method == 'POST' and request.form['filter'] == 'date':
        TransactQuery = Transactions.query.join(User, (Transactions.payer_id == User.id)).filter(or_(Transactions.payer_id == current_user.id, Transactions.payee_id == current_user.id)).filter(User.name.contains(request.form.get('search'))).order_by(Transactions.timestamp.desc())
    return render_template("user.html", name=current_user.name, money=current_user.money, transactform=transactform,
                           TransactionsHistory=TransactQuery, current_user_id=current_user.id, type=current_user.type)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
