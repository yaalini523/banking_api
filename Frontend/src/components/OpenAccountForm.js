import React, { Component } from "react";
import "./OpenAccountForm.css";
import { getHolderInfo, openAccount } from "../api/bankapi"; // import from bankapi.js

class OpenAccountForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      phone_number: "",
      holder_id: "",
      account_type: "",
      balance: "",
      generatedAccountNumber: "",
      loading: false,
      fetchingHolderId: false,
      error: "", // For inline errors
    };
  }

  //Updates the state when user types into form fields.
  handleChange = (e) => {
    this.setState({ [e.target.name]: e.target.value, error: "" });
  };

  fetchHolderId = async () => {
    const { phone_number } = this.state;
    if (!phone_number) return;

    this.setState({ fetchingHolderId: true, holder_id: "", error: "" });

    try {
      const res = await getHolderInfo(phone_number);

      if (res.data && res.data.holder_id) {
        this.setState({ holder_id: res.data.holder_id });
      } else {
        this.setState({ error: "No holder found with this phone number." });
      }
    } catch (err) {
      this.setState({
        error: "Error fetching holder ID. Please check the phone number.",
      });
      console.error(err);
    } finally {
      this.setState({ fetchingHolderId: false });
    }
  };

  handleSubmit = async (e) => {
    e.preventDefault();
    const { holder_id, account_type, balance } = this.state;

    this.setState({ loading: true, generatedAccountNumber: "", error: "" });

    if (!holder_id) {
      this.setState({ loading: false, error: "Valid holder ID required." });
      return;
    }

    try {
      const payload = { holder_id, account_type };
      if (balance) payload.balance = parseFloat(balance);

      const res = await openAccount(payload);

      if (res.data && res.data.account_number) {
        this.setState({
          generatedAccountNumber: res.data.account_number,
          error: "",
          phone_number: "",
          holder_id: "",
          account_type: "",
          balance: "",
        });
      } else {
        this.setState({ error: "Account created, but no account number returned." });
      }
    } catch (err) {
      this.setState({
        error: err.response?.data?.error || "Failed to open account due to network/server error.",
      });
      console.error("Error during account opening:", err);
    } finally {
      this.setState({ loading: false });
    }
  };

  render() {
    const { phone_number, holder_id, account_type, balance, generatedAccountNumber, loading, error } = this.state;

    return (
      <div className="open-account-container">
        <h2>Open Bank Account</h2>
        <form onSubmit={this.handleSubmit} className="open-account-form">
          <input
            name="phone_number"
            placeholder="Enter Phone Number"
            value={phone_number}
            onChange={this.handleChange}
            onBlur={this.fetchHolderId}
            required
          />

          <input
            name="holder_id"
            placeholder="Holder ID"
            value={holder_id}
            readOnly
            required
          />

          <select
            name="account_type"
            value={account_type}
            onChange={this.handleChange}
            required
          >
            <option value="">Select Account Type</option>
            <option value="Checking">Checking</option>
            <option value="Savings">Savings</option>
          </select>

          <input
            name="balance"
            placeholder="Initial Balance (optional)"
            value={balance}
            onChange={this.handleChange}
          />

          <button type="submit" disabled={loading}>
            {loading ? "Opening..." : "Open Account"}
          </button>

          {error && <p className="error-message">{error}</p>}
        </form>

        {generatedAccountNumber && (
          <p style={{ marginTop: "10px", color: "green" }}>
            Your account number: <strong>{generatedAccountNumber}</strong>
          </p>
        )}
      </div>
    );
  }
}

export default OpenAccountForm;
