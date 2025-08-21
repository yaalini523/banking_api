import React, { useState } from "react";
import "./CloseAccountForm.css";
import { closeAccount } from "../api/bankapi";

const CloseAccountForm = () => {
  const [accountId, setAccountId] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setAccountId(e.target.value);
    setMessage("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!accountId) {
      alert("Please enter an Account ID.");
      return;
    }

    const confirmClose = window.confirm(
      `Are you sure you want to close Account ID ${accountId}?`
    );
    if (!confirmClose) return;

    setLoading(true);
    try {
      const res = await closeAccount(accountId);

      const successMsg =
        res.data?.message || "Account closed successfully.";
      setMessage(successMsg);
      alert(successMsg);
      setAccountId(""); // reset input
    } catch (err) {
      const errorMsg =
        err.response?.data?.error || "Account closure failed due to server/network error.";
      alert(errorMsg);
      console.error("Error during account closure:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="close-account-container">
      <h2>Close Account</h2>
      <form onSubmit={handleSubmit} className="close-account-form">
        <input
          type="number"
          placeholder="Enter Account ID to Close"
          value={accountId}
          onChange={handleChange}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Closing..." : "Close Account"}
        </button>
      </form>

      {message && <div style={{ marginTop: "10px", color: "green" }}>{message}</div>}
    </div>
  );
};

export default CloseAccountForm;
