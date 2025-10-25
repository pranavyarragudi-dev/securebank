from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from banking_app import db
import random
import string


# ----------------------------------------------------------------------
# Role model (renamed to avoid Postgres "role" reserved keyword conflict)
# ----------------------------------------------------------------------
class Role(db.Model):
    __tablename__ = 'user_role'  # ✅ renamed from 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f'<Role {self.name}>'


# ----------------------------------------------------------------------
# User model
# ----------------------------------------------------------------------
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # ✅ updated foreign key reference to new table name
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), nullable=False)

    # Relationships
    role = db.relationship('Role', backref='users')
    accounts = db.relationship('Account', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role.name == 'admin'

    def is_customer(self):
        return self.role.name == 'customer'

    def __repr__(self):
        return f'<User {self.username}>'


# ----------------------------------------------------------------------
# Account model
# ----------------------------------------------------------------------
class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_type = db.Column(db.String(20), nullable=False)  # checking, savings
    balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    transactions_sent = db.relationship(
        'Transaction',
        foreign_keys='Transaction.from_account_id',
        backref='from_account',
        lazy='dynamic'
    )
    transactions_received = db.relationship(
        'Transaction',
        foreign_keys='Transaction.to_account_id',
        backref='to_account',
        lazy='dynamic'
    )

    def generate_account_number(self):
        return ''.join(random.choices(string.digits, k=10))

    def __init__(self, **kwargs):
        super(Account, self).__init__(**kwargs)
        if not self.account_number:
            self.account_number = self.generate_account_number()

    def get_transactions(self):
        sent = self.transactions_sent.all()
        received = self.transactions_received.all()
        all_transactions = sent + received
        return sorted(all_transactions, key=lambda x: x.created_at, reverse=True)

    def __repr__(self):
        return f'<Account {self.account_number}>'


# ----------------------------------------------------------------------
# Transaction model
# ----------------------------------------------------------------------
class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(20), nullable=False)  # transfer, deposit, withdrawal
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='completed')  # completed, pending, failed

    # For transfers
    from_account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    to_account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __repr__(self):
        return f'<Transaction {self.transaction_type}: ${self.amount}>'
