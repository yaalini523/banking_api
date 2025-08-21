from datetime import datetime, date
from db import SessionLocal
from models import Account
import re

def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def validate_dob(dob_str):
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        age = calculate_age(dob)
        if age < 18:
            return {'error': 'Account holder must be at least 18 years old'}, 400, None
        return None, None, dob
    except ValueError:
        return {'error': 'Invalid date format for dob. Use YYYY-MM-DD'}, 400, None

def validate_phone_number(phone):
    if not re.fullmatch(r'\d{10}', phone):
        return {'error': 'Invalid phone number format. Must be 10 digits'}, 400
    return None, None

def validate_aadhaar_number(aadhaar):
    if not re.fullmatch(r'\d{12}', aadhaar):
        return {'error': 'Invalid Aadhaar number format. Must be 12 digits'}, 400
    return None, None

def validate_email(email):
    if not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email):
        return {'error': 'Invalid email format'}, 400
    return None, None

def validate_account_type(account_type):
    valid_types = ['Checking', 'Savings']
    if account_type.capitalize() not in valid_types:
        return {'error': f'Invalid account type. Must be one of: {", ".join(valid_types)}'}, 400
    return None, 200

def get_account_by_id(account_id):
    session = SessionLocal()
    try:
        return session.get(Account, account_id)
    finally:
        session.close()

def update_account_balances(source, dest, amount):
    source.balance -= amount
    dest.balance += amount

def validate_account_closure(account):
    if not account:
        return {'error': 'Account not found'}, 404

    if account.status != 'Active':
        return {'error': 'Only Active accounts can be closed'}, 400

    if account.balance != 0.0:
        return {'error': 'Account cannot be closed unless balance is 0.00'}, 400

    return None, None
