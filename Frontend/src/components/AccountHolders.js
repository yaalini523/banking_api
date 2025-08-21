import React, { Component } from "react";
import { getAllHolders } from "../api/bankapi";
import "./AccountHolders.css";

class AccountHolders extends Component {
  state = {
    holders: [],
    error: "",
    authRole: "",
    loading: false,
  };

  handleInputChange = (e) => this.setState({ authRole: e.target.value });

  fetchHolders = async () => {
    const { authRole } = this.state;
    if (!authRole) {
      this.setState({ error: "Please enter an AuthRole before fetching." });
      return;
    }

    this.setState({ loading: true, error: "", holders: [] });

    try {
      const res = await getAllHolders(authRole);
      this.setState({ holders: res.data, error: "" });
    } catch (err) {
      this.setState({
        error: err.response?.data?.error || "Failed to fetch account holders.",
        holders: [],
      });
      console.error("Error fetching account holders:", err);
    } finally {
      this.setState({ loading: false });
    }
  };

  render() {
    const { holders, error, authRole, loading } = this.state;

    return (
      <div className="table-container">
        <div className="authrole-input">
          <label>AuthRole: </label>
          <input
            type="text"
            value={authRole}
            onChange={this.handleInputChange}
            placeholder="Enter role (e.g. Admin)"
          />
          <button onClick={this.fetchHolders} disabled={loading}>
            {loading ? "Fetching..." : "Fetch Account Holders"}
          </button>
        </div>

        {error && <div className="error">{error}</div>}

        {holders.length > 0 && (
          <table className="holder-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>First</th>
                <th>Last</th>
                <th>Email</th>
                <th>Phone</th>
                <th>DOB</th>
                <th>Aadhaar</th>
                <th>Address</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {holders.map((holder) => (
                <tr key={holder.id}>
                  <td>{holder.id}</td>
                  <td>{holder.first_name}</td>
                  <td>{holder.last_name}</td>
                  <td>{holder.email}</td>
                  <td>{holder.phone_number}</td>
                  <td>{holder.dob}</td>
                  <td>{holder.aadhaar_number}</td>
                  <td>{holder.address}</td>
                  <td>{holder.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    );
  }
}

export default AccountHolders;
