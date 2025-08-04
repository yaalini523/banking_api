from models import AccountHolder, Account

def test_close_account_success(client, session):
    holder = AccountHolder(
        first_name='John',
        last_name='Doe',
        dob='1985-05-10',
        address='Main Street',
        phone_number='9999999999',
        email='john.doe@example.com',
        aadhaar_number='123412341234'
    )
    session.add(holder)
    session.flush()

    account = Account(
        account_number='ACC001',
        account_type='Savings',
        holder_id=holder.id,
        balance=0.0,
        status='Active'
    )
    session.add(account)
    session.commit()

    response = client.post(f'/close_account/{account.id}')
    assert response.status_code == 200
    assert b'closed successfully' in response.data

def test_close_account_with_balance(client, session):
    holder = AccountHolder(
        first_name='Balance',
        last_name='Blocked',
        dob='1992-03-10',
        address='789 Money Rd',
        phone_number='8888888888',
        email='blocked@example.com',
        aadhaar_number='999988887777'
    )

    session.add(holder)
    session.flush()

    account = Account(
        account_number='BAL1234',
        account_type='Savings',
        holder_id=holder.id,
        balance=500.0
    )

    session.add(account)
    session.commit()

    response = client.post(f'/close_account/{account.id}')

    assert response.status_code == 400
    assert b'cannot be closed' in response.data.lower()
