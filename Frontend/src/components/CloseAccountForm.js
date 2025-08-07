import React, { useState } from "react";
import "./CloseAccountForm.css";
import axios from "axios";

const CloseAccountForm = () => {
  const [accountId, setAccountId] = useState("");
  const [message] = useState("");

  const handleChange = (e) => {
    setAccountId(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!accountId) {
      alert("Please enter an Account ID.");
      return;
    }

    const confirmClose = window.confirm(`Are you sure you want to close Account ID ${accountId}?`);
    if (!confirmClose) return;

    try {
      const res = await axios.delete(`http://localhost:5000/close_account/${accountId}`);
      if (res.data && res.data.message) {
        alert(res.data.message);
      } else {
        alert("Account closed successfully.");
      }
    } catch (err) {
      if (err.response && err.response.data && err.response.data.error) {
        alert(`Error: ${err.response.data.error}`);
      } else {
        alert("Account closure failed due to server/network error.");
      }
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
        <button type="submit">Close Account</button>
      </form>

      {message && <div>{message}</div>}
      
    </div>
  );
};

export default CloseAccountForm;
