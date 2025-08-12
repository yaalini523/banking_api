from flask import Flask, request, jsonify
from flask_cors import CORS
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from db import Base, engine
from auth import require_role
from validators.check_holder import register_account_holder, get_all_account_holders, get_holder_info_logic, get_accounts_by_holder_id
from validators.check_account import open_bank_account, close_account_by_id
from validators.check_transfer import process_fund_transfer

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

with app.app_context():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")


@app.route('/register', methods=['POST'])
def register():
    return register_account_holder(request.get_json())


@app.route("/get_holder_info", methods=["GET"])
def get_holder_info():
    phone = request.args.get("phone")
    info_type = request.args.get("type", "id")
    response, status = get_holder_info_logic(phone, info_type)
    return jsonify(response), status

@app.route("/get_accounts_by_holder/<int:holder_id>", methods=["GET"])
def get_accounts_by_holder(holder_id):
    data = {"holder_id": holder_id}
    result, status = get_accounts_by_holder_id(data)
    return jsonify(result), status


@app.route('/open_account', methods=['POST'])
def open_account():
    return open_bank_account(request.get_json())


@app.route('/account_holders', methods=['GET'])
@require_role('Admin')
def get_account_holders():
    return get_all_account_holders()

@app.route('/transfer', methods=['POST'])
def transfer_funds():
    data = request.get_json()
    return process_fund_transfer(data)

@app.route('/close_account/<int:account_id>', methods=['DELETE'])
def close_account(account_id):
    return close_account_by_id(account_id)

if __name__ == '__main__':
    app.run(debug=True)