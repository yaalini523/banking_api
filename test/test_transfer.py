import pytest
from unittest.mock import patch, MagicMock
from validators.check_transfer import process_fund_transfer
from models import Account, Transaction
from app import app

#Fixture to provide app context
@pytest.fixture
def mock_app_context():
    with app.app_context():
        yield

#Fixture to simulate database session with mock Accounts
@pytest.fixture
def mock_db_session():
    source = Account(id=1, balance=500.0, status="Active")
    dest = Account(id=2, balance=300.0, status="Active")

    #Creating a MagicMock DB session
    mock_db = MagicMock()

    #Using side_effect to return different mock queries for source and destination
    mock_db.query.return_value.filter_by.side_effect = [
        MagicMock(first=MagicMock(return_value=source)),  # for source_account
        MagicMock(first=MagicMock(return_value=dest))     # for destination_account
    ]

    return mock_db, source, dest

#Test for successful transfer
@patch("validators.check_transfer.SessionLocal")
@patch("validators.check_transfer.create_transfer_transactions")
@patch("validators.check_transfer.update_account_balances")
def test_successful_transfer(mock_update_bal, mock_create_txn, mock_session, mock_db_session):
    #Using return_value to return the mock session
    mock_db, source, dest = mock_db_session
    mock_session.return_value = mock_db

    # Define side effect function to simulate balance update
    def fake_update_balances(source_account, dest_account, amount):
        source_account.balance -= amount
        dest_account.balance += amount

    # Attach side effect to the mock
    mock_update_bal.side_effect = fake_update_balances
    
    #Fake txn creation inserts into mock_db instead of real DB
    def fake_create_txn(source_id, dest_id, amount):

        txn1 = Transaction(
            account_id=source_id,
            transaction_type="Debit",
            amount=amount,
            description="Test Debit",
            source_account_id=source_id,
            destination_account_id=dest_id
        )
        txn2 = Transaction(
            account_id=dest_id,
            transaction_type="Credit",
            amount=amount,
            description="Test Credit",
            source_account_id=source_id,
            destination_account_id=dest_id
        )
        mock_db.add_all([txn1, txn2])
        mock_db.commit()
        
        query_mock = MagicMock()
        filter_mock = MagicMock()
        filter_mock.first.return_value = txn1
        query_mock.filter_by.return_value = filter_mock
        mock_db.query.return_value = query_mock
        
    mock_create_txn.side_effect = fake_create_txn
    
    
    payload = {
        "source_account_id": 1,
        "destination_account_id": 2,
        "amount": 200.0
    }

    with app.app_context():
        response, status = process_fund_transfer(payload)
        
    assert status == 200
    assert "Transferred" in response.json["message"]
    #Verify balances are updated
    assert source.balance == 300.0
    assert dest.balance == 500.0
    
    #Check if transaction was stored
    txn = mock_db.query(Transaction).filter_by(
        source_account_id=1,
        destination_account_id=2,
        amount=200.0
    ).first()

    assert txn is not None
    assert txn.amount == 200.0

#Test for missing fields
@patch("validators.check_transfer.SessionLocal")
def test_missing_fields(mock_session, mock_app_context):
    payload = {
        "source_account_id": 1,
        "amount": 200.0  #Missing destination_account_id
    }
    response, status = process_fund_transfer(payload)
    assert status == 400
    assert "Missing fields" in response.json["error"]

#Test for invalid amount format
@patch("validators.check_transfer.SessionLocal")
def test_invalid_amount(mock_session, mock_app_context):
    payload = {
        "source_account_id": 1,
        "destination_account_id": 2,
        "amount": "invalid"  #Amount is not a number
    }
    response, status = process_fund_transfer(payload)
    assert status == 400
    assert "Invalid amount" in response.json["error"]

#Test for insufficient funds
@patch("validators.check_transfer.SessionLocal")
def test_insufficient_funds(mock_session, mock_app_context):
    source = Account(id=1, balance=100.0, status="Active")
    dest = Account(id=2, balance=500.0, status="Active")

    mock_db = MagicMock()
    
    #Using side_effect again to return source and destination accounts
    mock_db.query.return_value.filter_by.side_effect = [
        MagicMock(first=MagicMock(return_value=source)),
        MagicMock(first=MagicMock(return_value=dest))
    ]

    mock_session.return_value = mock_db  #return_value used again

    payload = {
        "source_account_id": 1,
        "destination_account_id": 2,
        "amount": 200.0
    }

    response, status = process_fund_transfer(payload)
    assert status == 400
    assert response.json["error"] == "Insufficient funds in source account"
