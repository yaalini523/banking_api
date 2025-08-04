from models import AccountHolder

def test_get_account_holders(client, session):
    holder = AccountHolder(
        first_name='Alice',
        last_name='Smith',
        dob='1995-05-05',
        address='Nowhere',
        phone_number='9999999999',
        email='alice@example.com',
        aadhaar_number='111122223333'
    )
    session.add(holder)
    session.commit()

    response = client.get('/account_holders', headers={'AuthRole': 'Admin'})
    assert response.status_code == 200
    
    data = response.get_json()

    assert isinstance(data, list)
    assert any(holder["email"] == "alice@example.com" for holder in data)
    assert any(holder["first_name"] == "Alice" for holder in data)

def test_get_account_holders_forbidden_role(client):
    response = client.get('/account_holders', headers={'AuthRole': 'User'})
    assert response.status_code == 403
    assert response.get_json()["error"] == "Forbidden: Insufficient permissions"

def test_get_account_holders_no_role_header(client):
    response = client.get('/account_holders')
    assert response.status_code == 403
    assert response.get_json()["error"] == "Forbidden: Insufficient permissions"

def test_get_account_holders_empty(client):
    response = client.get('/account_holders', headers={'AuthRole': 'Admin'})
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_account_holders_multiple(client, session):
    holders = [
        AccountHolder(
            first_name='Alice',
            last_name='Smith',
            dob='1990-01-01',
            address='City A',
            phone_number='1234567890',
            email='alice@example.com',
            aadhaar_number='111122223333'
        ),
        AccountHolder(
            first_name='Bob',
            last_name='Jones',
            dob='1988-03-12',
            address='City B',
            phone_number='0987654321',
            email='bob@example.com',
            aadhaar_number='444455556666'
        )
    ]
    session.add_all(holders)
    session.commit()

    response = client.get('/account_holders', headers={'AuthRole': 'Admin'})
    assert response.status_code == 200
    data = response.get_json()
    emails = [h['email'] for h in data]

    assert 'alice@example.com' in emails
    assert 'bob@example.com' in emails
