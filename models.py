from db import db 


class AccountHolder(db.Model):
    __tablename__ = 'account_holder'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    aadhaar_number = db.Column(db.String(12), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Active')

class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    holder_id = db.Column(db.Integer, db.ForeignKey('account_holder.id'), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    account_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Active')

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    description = db.Column(db.String(200))
    source_account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
    destination_account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)