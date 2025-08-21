import random
import string
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from db import SessionLocal
from models import AccountHolder, Account
from repo.db_repo import add_account, perform_account_closure
from logic.logic import validate_account_type, validate_account_closure


#Generate account number prefix based on type
def generate_account_number(account_type):
    random_digits = ''.join(random.choices(string.digits, k=7))  # exactly 7 digits
    if account_type.lower() == 'savings':
        return f"ACCS{random_digits}"
    elif account_type.lower() == 'checking':
        return f"ACC{random_digits}"
    else:
        return None
    

def open_bank_account(data):
    required_fields = ['holder_id', 'account_type']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    session = SessionLocal()
    try:
        holder = session.query(AccountHolder).filter_by(id=data['holder_id']).first()
        if not holder:
            return jsonify({'error': 'AccountHolder not found'}), 404

        # Validate account type
        error, status = validate_account_type(data['account_type'])
        if error:
            return jsonify(error), status

        # Generate unique account number
        account_number = generate_account_number(data['account_type'])
        while session.query(Account).filter_by(account_number=account_number).first():
            account_number = generate_account_number(data['account_type'])

        # Limit checking accounts
        if data['account_type'].lower() == 'checking':
            checking_count = session.query(Account).filter_by(
                holder_id=holder.id,
                account_type='Checking'
            ).count()
            if checking_count >= 2:
                return jsonify({'error': 'Limit reached: max 2 Checking accounts allowed'}), 400

        # Add new account
        account_data = {
            'holder_id': holder.id,
            'account_number': account_number,
            'account_type': data['account_type'],
            'balance': data.get('balance', 0.0)
        }
        add_account(account_data)
        session.commit()

        return jsonify({
            'message': 'Bank account created successfully',
            'account_number': account_number
        }), 201

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Failed to create account', 'details': str(e)}), 500
    finally:
        session.close()




def close_account_by_id(account_id):
    session = SessionLocal()
    try:
        account = session.query(Account).filter_by(id=account_id).first()

        error_response, status_code = validate_account_closure(account)
        if error_response:
            return jsonify(error_response), status_code

        closed_id = perform_account_closure(account_id)
        session.commit()

        return jsonify({'message': f'Account {closed_id} closed successfully'}), 200

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Account closure failed', 'details': str(e)}), 500

    finally:
        session.close()
