import React, { useState } from "react";
import './TransferForm.css';
import { transferFunds } from "../api/bankapi";

const TransferForm = () => {
  const [form, setForm] = useState({
    source_account_id: "",
    destination_account_id: "",
    amount: ""
  });
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setMessage("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.source_account_id || !form.destination_account_id || !form.amount) {
      alert("All fields are required.");
      return;
    }

    setLoading(true);
    try {
      const res = await transferFunds(form);

      const successMsg = res.data?.message || "Funds transferred successfully.";
      setMessage(successMsg);
      alert(successMsg);

      setForm({ source_account_id: "", destination_account_id: "", amount: "" }); // reset form
    } catch (err) {
      const errorMsg = err.response?.data?.error || "Transfer failed due to network/server error.";
      alert(errorMsg);
      console.error("Transfer error:", err);
    } finally {
      setLoading(false);
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
          value={form.source_account_id}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="destination_account_id"
          placeholder="Destination Account ID"
          value={form.destination_account_id}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="amount"
          placeholder="Amount"
          value={form.amount}
          onChange={handleChange}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Transferring..." : "Transfer"}
        </button>
      </form>

      {message && <div style={{ marginTop: "10px", color: "green" }}>{message}</div>}
    </div>
  );
};

export default TransferForm;
