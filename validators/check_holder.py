from flask import jsonify
from models import AccountHolder
from db import SessionLocal
from repo.db_repo import save_account_holder, fetch_all_account_holders
from logic.logic import (
    validate_dob, validate_phone_number, validate_aadhaar_number,
    validate_email
)

def register_account_holder(data):
    required_fields = ['first_name', 'last_name', 'dob', 'address', 'phone_number', 'email', 'aadhaar_number']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    # Validation
    error, status, dob = validate_dob(data['dob'])
    if error: return jsonify(error), status

    error, status = validate_phone_number(data['phone_number'])
    if error: return jsonify(error), status

    error, status = validate_aadhaar_number(data['aadhaar_number'])
    if error: return jsonify(error), status

    error, status = validate_email(data['email'])
    if error: return jsonify(error), status

    # Use raw SQLAlchemy session to check uniqueness
    session = SessionLocal()
    try:
        if session.query(AccountHolder).filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        if session.query(AccountHolder).filter_by(phone_number=data['phone_number']).first():
            return jsonify({'error': 'Phone number already registered'}), 400
        if session.query(AccountHolder).filter_by(aadhaar_number=data['aadhaar_number']).first():
            return jsonify({'error': 'Aadhaar number already registered'}), 400

        save_account_holder(data, dob, 'Active')
        return jsonify({'message': 'Account holder registered successfully'}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

def get_all_account_holders():
    holders = fetch_all_account_holders()
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