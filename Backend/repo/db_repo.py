from sqlalchemy.orm import Session
from models import AccountHolder, Account, Transaction
from db import SessionLocal

def save_account_holder(data, dob, status='Active'):
    session = SessionLocal()
    try:
        new_holder = AccountHolder(
        first_name=data['first_name'],
        last_name=data['last_name'],
        dob=dob,
        address=data['address'],
        phone_number=data['phone_number'],
        email=data['email'],
        aadhaar_number=data['aadhaar_number'],
        status=status
    )
        session.add(new_holder)
        session.commit()
        session.refresh(new_holder)
        return new_holder
    finally:
        session.close()

def add_account(data):
    session = SessionLocal()
    try:
        new_account = Account(
            account_number=data['account_number'],
            account_type=data['account_type'].capitalize(),
            holder_id=data['holder_id'],
            balance=data.get('balance', 0.0)
        )
        session.add(new_account)
        session.commit()
        session.refresh(new_account)
        return new_account
    finally:
        session.close()

def fetch_all_account_holders():
    session = SessionLocal()
    try:
        return session.query(AccountHolder).all()
    finally:
        session.close()

def create_transfer_transactions(source_id, dest_id, amount):
    session = SessionLocal()
    try:
        debit_transaction = Transaction(
            account_id=source_id,
            transaction_type='Debit',
            amount=amount,
            description=f'Transferred {amount:.2f} to Account {dest_id}',
            source_account_id=source_id,
            destination_account_id=dest_id
        )
        credit_transaction = Transaction(
            account_id=dest_id,
            transaction_type='Credit',
            amount=amount,
            description=f'Received {amount:.2f} from Account {source_id}',
            source_account_id=source_id,
            destination_account_id=dest_id
        )

        session.add_all([debit_transaction, credit_transaction])
        session.commit()
    finally:
        session.close()

def perform_account_closure(account_id):
    session = SessionLocal()
    try:
        account = session.get(Account, account_id)
        if not account:
            return None

        account.status = 'Closed'

        active_accounts = session.query(Account).filter(
            Account.holder_id == account.holder_id,
            Account.status == 'Active',
            Account.id != account.id
        ).count()

        if active_accounts == 0:
            holder = session.get(AccountHolder, account.holder_id)
            if holder:
                holder.status = 'Inactive'

        session.commit()
        return account.id
    finally:
        session.close()
