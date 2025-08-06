from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from db import SessionLocal
from models import AccountHolder, Account
from repo.db_repo import add_account, perform_account_closure
from logic.logic import validate_account_type, validate_account_closure


def open_bank_account(data):
    required_fields = ['holder_id', 'account_number', 'account_type']
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

        # Check account number uniqueness
        if session.query(Account).filter_by(account_number=data['account_number']).first():
            return jsonify({'error': 'Account number already exists'}), 400

        # Limit to 2 checking accounts
        if data['account_type'].lower() == 'checking':
            checking_count = session.query(Account).filter_by(holder_id=holder.id, account_type='Checking').count()
            if checking_count >= 2:
                return jsonify({'error': 'Limit reached: max 2 Checking accounts allowed'}), 400

        # Save account to DB
        add_account(data)
        session.commit()

        return jsonify({'message': 'Bank account created successfully'}), 201

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
