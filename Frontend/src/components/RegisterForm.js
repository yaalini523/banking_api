import React, { Component } from "react";
import "./RegisterForm.css";
import { registerHolder } from "../api/bankapi";

class RegisterForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      first_name: "",
      last_name: "",
      dob: "",
      address: "",
      phone_number: "",
      email: "",
      aadhaar_number: "",
      loading: false,
      error: "",
    };
  }

  handleChange = (e) => {
    this.setState({ [e.target.name]: e.target.value, error: "" });
  };

  handleSubmit = async (e) => {
    e.preventDefault();
    this.setState({ loading: true, error: "" });

    try {
      const res = await registerHolder(this.state);

      if (res.data && res.data.message) {
        alert(res.data.message);
      } else {
        alert("Registration successful!");
      }

      // Reset form after successful registration
      this.setState({
        first_name: "",
        last_name: "",
        dob: "",
        address: "",
        phone_number: "",
        email: "",
        aadhaar_number: "",
      });
    } catch (err) {
      const errorMsg = err.response?.data?.error || "Registration failed due to network/server error.";
      this.setState({ error: errorMsg });
      alert(errorMsg);
      console.error("Error during registration:", err);
    } finally {
      this.setState({ loading: false });
    }
  };

  render() {
    const { loading, error } = this.state;
    return (
      <div className="register-container">
        <h2>Register Account Holder</h2>
        <form onSubmit={this.handleSubmit} className="register-form">
          <input
            name="first_name"
            placeholder="First Name"
            value={this.state.first_name}
            onChange={this.handleChange}
            required
          />
          <input
            name="last_name"
            placeholder="Last Name"
            value={this.state.last_name}
            onChange={this.handleChange}
            required
          />
          <input
            type="date"
            name="dob"
            value={this.state.dob}
            onChange={this.handleChange}
            required
          />
          <input
            name="address"
            placeholder="Address"
            value={this.state.address}
            onChange={this.handleChange}
            required
          />
          <input
            name="phone_number"
            placeholder="Phone Number"
            value={this.state.phone_number}
            onChange={this.handleChange}
            required
          />
          <input
            name="email"
            placeholder="Email"
            value={this.state.email}
            onChange={this.handleChange}
            required
          />
          <input
            name="aadhaar_number"
            placeholder="Aadhaar Number"
            value={this.state.aadhaar_number}
            onChange={this.handleChange}
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? "Registering..." : "Register"}
          </button>
        </form>
        {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
      </div>
    );
  }
}

export default RegisterForm;
