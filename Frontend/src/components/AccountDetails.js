import React, { useState } from "react";
import { getAccountsByHolder } from "../api/bankapi";
import "./AccountHolders.css";

function AccountDetails() {
  const [holderId, setHolderId] = useState("");
  const [accountDetails, setAccountDetails] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchAccountDetails = async () => {
    setError("");
    setAccountDetails([]);

    if (!holderId) {
      setError("Please enter holder ID.");
      return;
    }

    setLoading(true);
    try {
      const res = await getAccountsByHolder(holderId);
      if (res.data && res.data.accounts && res.data.accounts.length > 0) {
        setAccountDetails(res.data.accounts);
      } else {
        setError("No accounts found for this holder.");
      }
    } catch (err) {
      setError(err.response?.data?.error || "Failed to fetch account details.");
      console.error("Error fetching accounts:", err);
    } finally {
      setLoading(false);
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
      <button onClick={fetchAccountDetails} disabled={loading}>
        {loading ? "Fetching..." : "Fetch Account Details"}
      </button>

      {accountDetails.length > 0 && (
        <div style={{ border: "1px solid #ccc", padding: "10px", marginTop: "20px" }}>
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
        </div>
      )}

      {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
    </div>
  );
}

export default AccountDetails;
