import React, { useState } from "react";
import './TransferForm.css';
import axios from "axios";

const TransferForm = () => {
  const [form, setForm] = useState({
    source_account_id: "",
    destination_account_id: "",
    amount: ""
  });

  const [message] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await axios.post("http://localhost:5000/transfer", form);

      if (res.data && res.data.message) {
        alert(res.data.message);
      } else {
        alert("Funds transferred successfully.");
      }
    } catch (err) {
      if (err.response && err.response.data && err.response.data.error) {
        alert(err.response.data.error);
      } else {
        alert("Transfer failed due to network/server error.");
      }
      console.error("Transfer error:", err);
    }
  };

  return (
    <div className="transfer-container">
      <h2>Transfer Funds</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="source_account_id"
          placeholder="Source Account ID"
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="destination_account_id"
          placeholder="Destination Account ID"
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="amount"
          placeholder="Amount"
          onChange={handleChange}
          required
        />
        <button type="submit">Transfer</button>
      </form>

      {message && <div>{message}</div>}
      
    </div>
  );
};

export default TransferForm;
