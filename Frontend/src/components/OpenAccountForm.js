import React, { useState } from "react";
import "./OpenAccountForm.css";
import axios from "axios";

const OpenAccountForm = () => {
  const [form, setForm] = useState({
    holder_id: "",
    account_number: "",
    account_type: "",
    balance: ""
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        holder_id: form.holder_id,
        account_number: form.account_number,
        account_type: form.account_type,
      };

      if (form.balance) {
        payload.balance = parseFloat(form.balance);
      }

      const res = await axios.post("http://localhost:5000/open_account", payload);

      if (res.data && res.data.message) {
        alert(res.data.message);
      } else {
        alert("Account opened successfully!");
      }
    } catch (err) {
      if (err.response && err.response.data && err.response.data.error) {
        alert(err.response.data.error);
      } else {
        alert("Failed to open account due to network/server error.");
      }
      console.error("Error during account opening:", err);
    }
  };

  return (
    <div className="open-account-container">
      <h2>Open Bank Account</h2>
      <form onSubmit={handleSubmit} className="open-account-form">
        <input
          name="holder_id"
          placeholder="Holder ID"
          value={form.holder_id}
          onChange={handleChange}
          required
        />
        <input
          name="account_number"
          placeholder="Account Number"
          value={form.account_number}
          onChange={handleChange}
          required
        />
        <select
          name="account_type"
          value={form.account_type}
          onChange={handleChange}
          required
        >
          <option value="">Select Account Type</option>
          <option value="Checking">Checking</option>
          <option value="Savings">Savings</option>
        </select>
        <input
          name="balance"
          placeholder="Initial Balance (optional)"
          value={form.balance}
          onChange={handleChange}
        />
        <button type="submit">Open Account</button>
      </form>
    </div>
  );
};

export default OpenAccountForm;
