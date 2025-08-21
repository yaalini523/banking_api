import React, { useState } from "react";
import { getHolderInfo } from "../api/bankapi";

function AccountHolderDetails() {
  const [phone, setPhone] = useState("");
  const [holderDetails, setHolderDetails] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchHolderDetails = async () => {
    setError("");
    setHolderDetails(null);

    if (!phone) {
      setError("Please enter a phone number.");
      return;
    }

    setLoading(true);
    try {
      const res = await getHolderInfo(phone);

      if (res.data && res.data.id) {
        setHolderDetails(res.data);
      } else {
        setError("No holder found with this phone number.");
      }
    } catch (err) {
      setError(err.response?.data?.error || "Failed to fetch holder details.");
      console.error("Error fetching holder details:", err);
    } finally {
      setLoading(false);
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
      <button onClick={fetchHolderDetails} disabled={loading}>
        {loading ? "Fetching..." : "Fetch Holder Details"}
      </button>

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
