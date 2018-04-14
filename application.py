from flask import Flask, render_template, url_for, request, session, redirect
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Email, InputRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = 'Shhh!It\'s a sceret'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database/userdetails.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
Session(app)
# TODO Modularize database
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    # TODO Validate phone number
    phone = IntegerField('PhoneNumber', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=15, message="Insufficient password length")])
    submit = SubmitField("Log In")


class RegisterForm(FlaskForm):
    phone = IntegerField('PhoneNumber', validators=[InputRequired()])
    name = StringField('name', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Email()])
    password = PasswordField('password', validators=[InputRequired()])
    submit = SubmitField("Register")


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return render_template("user.html", name=request.form.get(""))
    else:
        form = RegisterForm()
        return render_template("home.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for("user_dashboard"))
        return "<h1>" + str(form.phone.data) + "" + form.password.data + "</h1>"

    return render_template("home.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if request.method == 'GET':
        return render_template("home.html", form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new = User(name=form.name.data, phone=form.phone.data, email=form.email.data, password=hashed_password)
            db.session.add(new)
            db.session.commit()
            return "will create user here"
            # if ' user already exist in the database':
            #     return "Email address already exists"
            # else:
        else:
            return "Form didn't validate"
    return render_template("")


# TODO change user's url
@app.route("/user/dashboard", methods=["GET", "POST"])
@login_required
def user_dashboard():
    if session.get("money") is None:
        session["money"] = 0
    if request.method == "POST":
        session["money"] += int(request.form.get("add"))
    return render_template("user.html", name=current_user.name, money=session["money"])


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
def init_db():
    db.init_app(app)
    db.app = app
    # db.drop_all()
    db.create_all()


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
