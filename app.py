from flask import Flask, request, jsonify
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from db import db
from models import AccountHolder, Account, Transaction
from auth import require_role
from sqlalchemy.exc import SQLAlchemyError
import re
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

with app.app_context():
    db.create_all()
    print("Tables created successfully")


def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


@app.route('/register', methods=['POST'])
def register_account_holder():
    data = request.get_json()
    
    required_fields = ['first_name', 'last_name', 'dob', 'address', 'phone_number', 'email', 'aadhaar_number']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
    
    try:
        dob = datetime.strptime(data['dob'], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'error': 'Invalid date format for dob. Use YYYY-MM-DD'}), 400
    
    if not re.fullmatch(r'\d{10}', data['phone_number']):
        return jsonify({'error': 'Invalid phone number format. Must be 10 digits'}), 400

    if not re.fullmatch(r'\d{12}', data['aadhaar_number']):
        return jsonify({'error': 'Invalid Aadhaar number format. Must be 12 digits'}), 400
    
    if not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    age = calculate_age(dob)
    if age < 18:
        return jsonify({'error': 'Account holder must be at least 18 years old'}), 400
    
    if AccountHolder.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400

    if AccountHolder.query.filter_by(phone_number=data['phone_number']).first():
        return jsonify({'error': 'Phone number already registered'}), 400

    if AccountHolder.query.filter_by(aadhaar_number=data['aadhaar_number']).first():
        return jsonify({'error': 'Aadhaar number already registered'}), 400

    new_holder = AccountHolder(
        first_name=data['first_name'],
        last_name=data['last_name'],
        dob=dob,
        address=data['address'],
        phone_number=data['phone_number'],
        email=data['email'],
        aadhaar_number=data['aadhaar_number']
    )
    
    db.session.add(new_holder)
    db.session.commit()
    
    return jsonify({'message': 'Account holder registered successfully'}), 201

@app.route('/open_account', methods=['POST'])
def open_account():
    data = request.get_json()
    
    required_fields = ['holder_id', 'account_number', 'account_type']
    missing = [field for field in required_fields if field not in data]
    
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400
    
    holder = db.session.get(AccountHolder, data['holder_id'])
    
    if not holder:
        return jsonify({'error': 'AccountHolder not found'}), 404
    
    if data['account_type'].lower() == 'checking':
        checking_count = Account.query.filter_by(holder_id=holder.id, account_type='Checking').count()
        if checking_count >= 2:
            return jsonify({'error': 'Limit reached: AccountHolder can have max 2 Checking accounts'}), 400
    
    if Account.query.filter_by(account_number=data['account_number']).first():
        return jsonify({'error': 'Account number already exists'}), 400

    new_account = Account(
        account_number=data['account_number'],
        account_type=data['account_type'],
        holder_id=holder.id
    )

    db.session.add(new_account)
    db.session.commit()

    return jsonify({'message': 'Bank account created successfully'}), 201


@app.route('/account_holders', methods=['GET'])
@require_role('Admin')
def get_account_holders():
    holders = AccountHolder.query.all()
    result = []
    for holder in holders:
        result.append({
            'id': holder.id,
            'first_name': holder.first_name,
            'last_name': holder.last_name,
            'email': holder.email,
            'phone_number': holder.phone_number,
            'dob': holder.dob.isoformat(),
            'aadhaar_number': holder.aadhaar_number,
            'address': holder.address
        })
    return jsonify(result), 200


@app.route('/transfer', methods=['POST'])
def transfer_funds():
    data = request.get_json()

    required_fields = ['source_account_id', 'destination_account_id', 'amount']
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({'error': 'Amount must be greater than zero'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400
    
    source = db.session.get(Account, data['source_account_id'])
    dest = db.session.get(Account, data['destination_account_id'])


    if not source or not dest:
        return jsonify({'error': 'One or both accounts not found'}), 404

    if source.status != 'Active' or dest.status != 'Active':
        return jsonify({'error': 'Both accounts must be Active'}), 400

    if source.balance < amount:
        return jsonify({'error': 'Insufficient funds in source account'}), 400
    
    try:
        source.balance -= amount
        dest.balance += amount

        
        debit_transaction = Transaction(
            account_id=source.id,
            transaction_type='Debit',
            amount=amount,
            description=f'Transferred {amount:.2f} to Account {dest.id}',
            source_account_id=source.id,
            destination_account_id=dest.id
        )
        credit_transaction = Transaction(
            account_id=dest.id,
            transaction_type='Credit',
            amount=amount,
            description=f'Received {amount:.2f} from Account {source.id}',
            source_account_id=source.id,
            destination_account_id=dest.id
        )

        db.session.add(debit_transaction)
        db.session.add(credit_transaction)
        db.session.commit()

        return jsonify({'message': f'Transferred {amount:.2f} from Account {source.id} to Account {dest.id}'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Transfer failed', 'details': str(e)}), 500

@app.route('/close_account/<int:account_id>', methods=['POST'])
def close_account(account_id):
    try:
        account = db.session.get(Account, account_id)
        if not account:
            return jsonify({'error': 'Account not found'}), 404

        if account.status != 'Active':
            return jsonify({'error': 'Only Active accounts can be closed'}), 400

        if account.balance != 0.0:
            return jsonify({'error': 'Account cannot be closed unless balance is 0.00'}), 400

    
        account.status = 'Closed'

        print(f"Closing account: {account.id}")
        print(f"Holder ID: {account.holder_id}")
        
        active_accounts = Account.query.filter(
            Account.holder_id == account.holder_id,
            Account.status == 'Active',
            Account.id != account.id
        ).count()
        
        print(f"Other active accounts: {active_accounts}")

        if active_accounts == 0:
            holder = db.session.get(AccountHolder, account.holder_id)
            if holder:
                print("Setting holder status to Inactive")
                holder.status = 'Inactive'

        db.session.commit()

        return jsonify({'message': f'Account {account_id} closed successfully'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Account closure failed', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)