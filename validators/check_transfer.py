from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from db import SessionLocal
from models import Account
from repo.db_repo import create_transfer_transactions
from logic.logic import get_account_by_id, update_account_balances

def process_fund_transfer(data):
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

    session = SessionLocal()

    try:
        # Get IDs from the request
        source_id = int(data['source_account_id'])
        dest_id = int(data['destination_account_id'])

        # Fetch accounts using ID
        source = session.query(Account).filter_by(id=source_id).first()
        dest = session.query(Account).filter_by(id=dest_id).first()

        if not source or not dest:
            return jsonify({'error': 'One or both accounts not found'}), 404

        if source.status != 'Active' or dest.status != 'Active':
            return jsonify({'error': 'Both accounts must be Active'}), 400

        if source.balance < amount:
            return jsonify({'error': 'Insufficient funds in source account'}), 400

        # Update balances
        update_account_balances(source, dest, amount)

        # Create transactions
        create_transfer_transactions(source.id, dest.id, amount)

        # Commit changes
        session.commit()

        return jsonify({
            'message': f'Transferred {amount:.2f} from Account {source.id} to Account {dest.id}'
        }), 200

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Transfer failed', 'details': str(e)}), 500

    finally:
        session.close()
