from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# ORM Database Table: Class | Row: Object | Column: Properties
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    money = db.Column(db.Integer, default=0)

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)