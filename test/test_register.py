import json
import pytest

valid_base_data = {
    "first_name": "Test",
    "last_name": "User",
    "dob": "1990-01-01",
    "address": "Some Address",
    "phone_number": "9999999999",
    "email": "testuser@example.com",
    "aadhaar_number": "999988887777"
}

def test_register_valid_holder(client):
    response = client.post("/register", data=json.dumps(valid_base_data), content_type="application/json")
    assert response.status_code == 201
    assert response.get_json()["message"] == "Account holder registered successfully"

def test_register_missing_fields(client):
    response = client.post("/register", data=json.dumps({"first_name": "John"}), content_type="application/json")
    assert response.status_code == 400
    assert "Missing fields" in response.get_json()["error"]

def test_register_invalid_age(client):
    data = valid_base_data.copy()
    data["dob"] = "2010-01-01"  # Age < 18
    response = client.post("/register", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert response.get_json()["error"] == "Account holder must be at least 18 years old"

def test_register_invalid_email(client):
    data = valid_base_data.copy()
    data["email"] = "invalid_email"
    response = client.post("/register", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid email format"

def test_register_invalid_phone(client):
    data = valid_base_data.copy()
    data["phone_number"] = "12345"
    response = client.post("/register", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid phone number format. Must be 10 digits"

def test_register_invalid_aadhaar(client):
    data = valid_base_data.copy()
    data["aadhaar_number"] = "12345"
    response = client.post("/register", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid Aadhaar number format. Must be 12 digits"

def test_register_invalid_dob_format(client):
    data = valid_base_data.copy()
    data["dob"] = "01-01-1990"  # Wrong format
    response = client.post("/register", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid date format for dob. Use YYYY-MM-DD"

def test_register_duplicate_email(client, session):
    # First registration
    session.commit()
    client.post("/register", data=json.dumps(valid_base_data), content_type="application/json")
    
    # Second registration with same email
    data = valid_base_data.copy()
    data["aadhaar_number"] = "123456789111"
    data["phone_number"] = "8888888888"
    response = client.post("/register", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert response.get_json()["error"] == "Email already registered"

def test_register_duplicate_aadhaar(client, session):
    session.commit()
    client.post("/register", data=json.dumps(valid_base_data), content_type="application/json")
    
    data = valid_base_data.copy()
    data["email"] = "newemail@example.com"
    data["phone_number"] = "7777777777"
    response = client.post("/register", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert response.get_json()["error"] == "Aadhaar number already registered"
