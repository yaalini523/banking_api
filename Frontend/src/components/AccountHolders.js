import React, { useEffect, useState } from "react";
import axios from "axios";
import "./AccountHolders.css";

const AccountHolders = () => {
  const [holders, setHolders] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchHolders = async () => {
      try {
        const res = await axios.get("http://localhost:5000/account_holders", {
          headers: {
            AuthRole: "Admin" // Change if needed
          }
        });
        setHolders(res.data);
      } catch (err) {
        setError(err.response?.data?.error || "Failed to fetch account holders.");
      }
    };

    fetchHolders();
  }, []);

  if (error) return <div className="error">{error}</div>;
  if (holders.length === 0) return <p>No account holders found.</p>;

  return (
    <div className="table-container">
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
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AccountHolders;
