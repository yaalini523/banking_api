import React, { useState } from "react";
import axios from "axios";
import "./AccountHolders.css";

function AccountDetails() {
  const [holderId, setHolderId] = useState("");
  const [accountDetails, setAccountDetails] = useState(null);
  const [error, setError] = useState("");

  const fetchAccountDetails = async () => {
    setError("");
    setAccountDetails(null);

    if (!holderId) {
      setError("Please enter holder ID.");
      return;
    }

    try {
      const res = await axios.get(
        `http://localhost:5000/get_accounts_by_holder/${holderId}`
      );
      setAccountDetails(res.data.accounts || []);  // Assuming your backend returns {'accounts': [...]}
    } catch (err) {
      setError(err.response?.data?.error || "No accounts found for this holder_id");
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "auto" }}>
      <h2>Account Details</h2>

      <input
        type="text"
        placeholder="Enter Holder ID"
        value={holderId}
        onChange={(e) => setHolderId(e.target.value)}
      />
      <button onClick={fetchAccountDetails}>Fetch Account Details</button>

      {accountDetails && (
        <div style={{ border: "1px solid #ccc", padding: "10px", marginTop: "20px" }}>
          {accountDetails.length > 0 ? (
            <table border="1" cellPadding="5" cellSpacing="0" style={{ width: "100%" }}>
              <thead>
                <tr>
                  <th>Id</th>
                  <th>Account Number</th>
                  <th>Account Type</th>
                  <th>Balance</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {accountDetails.map((acc) => (
                  <tr key={acc.account_number}>
                    <td>{acc.id}</td>
                    <td>{acc.account_number}</td>
                    <td>{acc.account_type}</td>
                    <td>{acc.balance}</td>
                    <td>{acc.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No accounts found for this holder.</p>
          )}
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default AccountDetails;
