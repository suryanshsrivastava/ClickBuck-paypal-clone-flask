from app import db
from flask_sqlalchemy import event
from sqlalchemy import engine
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from datetime import datetime


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# noinspection PyUnusedLocal
@event.listens_for(engine.Engine, 'connect')
def __set_sqlite_pragma(db_conn, conn_record):
    cursor = db_conn.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    cursor.close()

class Transactions(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    payer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    payee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    amount = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

# Transactions = db.Table('transactions',
#                         db.Column('payer_id', db.Integer, db.ForeignKey('users.id')),
#                         db.Column('payee_id', db.Integer, db.ForeignKey('users.id')),
#                         db.Column('amount', db.Integer),
#                         db.Column('timestamp', db.DateTime, index=True, default=datetime.utcnow)
#                         )


# ORM Database Table: Class | Row: Object | Column: Properties
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.Integer, nullable=False, index=True, unique=True)
    type = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False, index=True, unique=True)
    password = db.Column(db.String(80), nullable=False)
    money = db.Column(db.Integer, default=0)
    transaction_paid = db.relationship('Transactions', backref=db.backref('paid'), primaryjoin=id == Transactions.payer_id)
    transaction_received = db.relationship('Transactions', backref=db.backref('received'), primaryjoin=id == Transactions.payee_id)

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


