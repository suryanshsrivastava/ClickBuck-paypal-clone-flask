from flask import render_template, flash, url_for, request, redirect
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import or_, and_
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
    Requests = Transactions.query.join(User, (Transactions.payer_id == User.id)).filter(and_(Transactions.done == 0, Transactions.payer_id == current_user.id)).order_by(Transactions.timestamp.desc())

    # Add Money feature
    if request.method == "POST" and transactform.addbutton.data:
        current_user.money += int(transactform.add.data)
        db.session.commit()
        return redirect(url_for('user_dashboard'))

    # Pay/Receive feature
    if request.method == "POST":
        if transactform.paybutton.data:
            payee = User.query.filter_by(phone=transactform.payee.data).first()
            transact = Transactions(payer_id=current_user.id, payee_id=payee.id, amount=int(transactform.pay.data))
            current_user.money -= int(transactform.pay.data)
            payee.money += int(transactform.pay.data)
            transact.done = 1
            db.session.add(transact)
        if transactform.receivebutton.data:
            payer = User.query.filter_by(phone=transactform.payer.data).first()
            transact = Transactions(payer_id=payer.id, payee_id=current_user.id, amount=int(transactform.receive.data))
            db.session.add(transact)
        if 'accept' in request.form.values():
            transact = Transactions.query.filter_by(id=request.form.get('request_id')).first()
            payee = User.query.filter_by(id=transact.payee_id).first()
            current_user.money -= int(transact.amount)
            payee.money += int(transact.amount)
            transact.done = 1
        if 'decline' in request.form.values():
            Transactions.query.filter_by(id=request.form.get('request_id')).delete()
        db.session.commit()

        return redirect(url_for('user_dashboard'))


    # Request someone
    if request.method == 'POST' and request.form['filter'] == 'string':
        print('string request')
        TransactQuery = Transactions.query.join(User, (Transactions.payer_id == User.id)).filter(or_(Transactions.payer_id == current_user.id, Transactions.payee_id == current_user.id)).filter(Transactions.timestamp.between(request.form.get('from'), request.form.get('to'))).order_by(Transactions.timestamp.desc())
    if request.method == 'POST' and request.form['filter'] == 'date':
        print('date request')
        TransactQuery = Transactions.query.join(User, (Transactions.payer_id == User.id)).filter(or_(Transactions.payer_id == current_user.id, Transactions.payee_id == current_user.id)).filter(User.name.contains(request.form.get('search'))).order_by(Transactions.timestamp.desc())
    return render_template("user.html", name=current_user.name, money=current_user.money, transactform=transactform,
                           TransactionsHistory=TransactQuery, current_user_id=current_user.id, type=current_user.type,
                           requests_pending=Requests)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
