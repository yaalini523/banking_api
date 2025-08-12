import React, { useState } from "react";
import axios from "axios";
import "./AccountHolders.css";

function AccountHolderDetails() {
  const [phone, setPhone] = useState("");
  const [holderDetails, setHolderDetails] = useState(null);
  const [error, setError] = useState("");

  const fetchHolderDetails = async () => {
    setError("");
    setHolderDetails(null);

    if (!phone) {
      setError("Please enter a phone number.");
      return;
    }

    try {
      const res = await axios.get("http://localhost:5000/get_holder_info", {
        params: { phone, type: "details" },
      });
      setHolderDetails(res.data);
    } catch (err) {
      setError(err.response?.data?.error || "Failed to fetch holder details.");
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "auto" }}>
      <h2>Account Holder Details</h2>

      <input
        type="text"
        placeholder="Enter Phone Number"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
      />
      <button onClick={fetchHolderDetails}>Fetch Holder Details</button>

      {holderDetails && (
        <div style={{ border: "1px solid #ccc", padding: "10px", marginTop: "20px" }}>
          <p><b>ID:</b> {holderDetails.id}</p>
          <p><b>Name:</b> {holderDetails.first_name} {holderDetails.last_name}</p>
          <p><b>Email:</b> {holderDetails.email}</p>
          <p><b>Phone:</b> {holderDetails.phone_number}</p>
          <p><b>DOB:</b> {holderDetails.dob}</p>
          <p><b>Aadhaar:</b> {holderDetails.aadhaar_number}</p>
          <p><b>Address:</b> {holderDetails.address}</p>
          <p><b>Status:</b> {holderDetails.status}</p>
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default AccountHolderDetails;
