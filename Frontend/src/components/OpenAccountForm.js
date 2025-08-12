import React, { Component } from "react";
import "./OpenAccountForm.css";
import axios from "axios";

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
    };
  }

  handleChange = (e) => {
    this.setState({ [e.target.name]: e.target.value });
  };

  // Fetch holder_id when phone number is entered
  fetchHolderId = async () => {
    if (!this.state.phone_number) return;

    this.setState({ fetchingHolderId: true, holder_id: "" });

    try {
      const res = await axios.get(
        "http://localhost:5000/get_holder_info",
        {
          params: { phone: this.state.phone_number },
        }
      );

      if (res.data && res.data.holder_id) {
        this.setState({ holder_id: res.data.holder_id });
      } else {
        alert("No holder found with this phone number.");
      }
    } catch (err) {
      alert("Error fetching holder ID. Please check the phone number.");
      console.error(err);
    } finally {
      this.setState({ fetchingHolderId: false });
    }
  };

  handleSubmit = async (e) => {
    e.preventDefault();
    this.setState({ loading: true, generatedAccountNumber: "" });

    try {
      const payload = {
        holder_id: this.state.holder_id,
        account_type: this.state.account_type,
      };

      if (this.state.balance) {
        payload.balance = parseFloat(this.state.balance);
      }

      const res = await axios.post(
        "http://localhost:5000/open_account",
        payload
      );

      if (res.data && res.data.account_number) {
        alert(`Account created successfully!`);
        this.setState({ generatedAccountNumber: res.data.account_number });
      } else {
        alert("Account created, but no account number returned.");
      }
    } catch (err) {
      if (err.response?.data?.error) {
        alert(err.response.data.error);
      } else {
        alert("Failed to open account due to network/server error.");
      }
      console.error("Error during account opening:", err);
    } finally {
      this.setState({ loading: false });
    }
  };

  render() {
    return (
      <div className="open-account-container">
        <h2>Open Bank Account</h2>
        <form onSubmit={this.handleSubmit} className="open-account-form">
          {/* Phone number field to get holder_id */}
          <input
            name="phone_number"
            placeholder="Enter Phone Number"
            value={this.state.phone_number}
            onChange={this.handleChange}
            onBlur={this.fetchHolderId}
            required
          />

          {/* Holder ID (auto-filled) */}
          <input
            name="holder_id"
            placeholder="Holder ID"
            value={this.state.holder_id}
            readOnly
            required
          />

          <select
            name="account_type"
            value={this.state.account_type}
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
            value={this.state.balance}
            onChange={this.handleChange}
          />

          <button type="submit" disabled={this.state.loading}>
            {this.state.loading ? "Opening..." : "Open Account"}
          </button>
        </form>

        {/* Show generated account number below button */}
        {this.state.generatedAccountNumber && (
          <p style={{ marginTop: "10px", color: "green" }}>
            Your account number:{" "}
            <strong>{this.state.generatedAccountNumber}</strong>
          </p>
        )}
      </div>
    );
  }
}

export default OpenAccountForm;
