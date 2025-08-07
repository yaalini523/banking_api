import React, { useState } from "react";
import './RegisterForm.css';
import axios from "axios";

const RegisterForm = () => {
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    dob: "",
    address: "",
    phone_number: "",
    email: "",
    aadhaar_number: ""
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:5000/register", form);

      if (res.data && res.data.message) {
        alert(res.data.message);
      } else {
        alert("Registration successful!");
      }
    } catch (err) {
      if (err.response && err.response.data && err.response.data.error) {
        alert(err.response.data.error);
      } else {
        alert("Registration failed due to network/server error.");
      }
      console.error("Error during registration:", err);
    }
  };

  return (
    <div className="register-container">
      <h2>Register Account Holder</h2>
      <form onSubmit={handleSubmit} className="register-form">
        <input name="first_name" placeholder="First Name" onChange={handleChange} required />
        <input name="last_name" placeholder="Last Name" onChange={handleChange} required />
        <input type="date" name="dob" onChange={handleChange} required />
        <input name="address" placeholder="Address" onChange={handleChange} required />
        <input name="phone_number" placeholder="Phone Number" onChange={handleChange} required />
        <input name="email" placeholder="Email" onChange={handleChange} required />
        <input name="aadhaar_number" placeholder="Aadhaar Number" onChange={handleChange} required />
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default RegisterForm;
