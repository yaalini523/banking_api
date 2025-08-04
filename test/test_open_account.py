import pytest
import json
from models import AccountHolder, Account

@pytest.fixture
def create_holder(session):
    def _create_holder():
        holder = AccountHolder(
            first_name='Arjun',
            last_name='Dev',
            dob='1990-01-01',
            address='456 Road',
            phone_number='9998887777',
            email='testuser@example.com',
            aadhaar_number='111122223333'
        )
        session.add(holder)
        session.commit()
        return holder
    return _create_holder

def test_open_account_success(client, session, create_holder):
    holder = create_holder()

    response = client.post('/open_account', json={
        'holder_id': holder.id,
        'account_number': 'AC123456',
        'account_type': 'Checking'
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Bank account created successfully'

def test_open_account_missing_fields(client):
    response = client.post('/open_account', json={
        'account_type': 'Checking'
    })

    assert response.status_code == 400
    data = response.get_json()
    assert "Missing fields" in data['error']
    assert "holder_id" in data['error'] and "account_number" in data['error']

def test_open_account_invalid_holder(client):
    response = client.post('/open_account', json={
        'holder_id': 999,
        'account_number': 'XYZ12345',
        'account_type': 'Checking'
    })

    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'AccountHolder not found'

def test_open_account_duplicate_account_number(client, session, create_holder):
    holder = create_holder()
    # First account
    account = Account(account_number='DUPL1234', account_type='Savings', holder_id=holder.id)
    session.add(account)
    session.commit()

    # Second account with same number
    response = client.post('/open_account', json={
        'holder_id': holder.id,
        'account_number': 'DUPL1234',
        'account_type': 'Checking'
    })

    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Account number already exists'

def test_open_account_limit_checking_accounts(client, session, create_holder):
    holder = create_holder()

    # Add 2 checking accounts
    session.add_all([
        Account(account_number='CHK1001', account_type='Checking', holder_id=holder.id),
        Account(account_number='CHK1002', account_type='Checking', holder_id=holder.id)
    ])
    session.commit()

    # Third checking account (should fail)
    response = client.post('/open_account', json={
        'holder_id': holder.id,
        'account_number': 'CHK1003',
        'account_type': 'Checking'
    })

    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Limit reached: AccountHolder can have max 2 Checking accounts'
