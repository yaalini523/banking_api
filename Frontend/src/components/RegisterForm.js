import React, { Component } from "react";
import "./RegisterForm.css";
import axios from "axios";

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
      aadhaar_number: ""
    };
  }

  // reading the values -> name: value
  handleChange = (e) => {
    this.setState({ [e.target.name]: e.target.value });
  };

  handleSubmit = async (e) => {
    // prevents from refreshing the page after submit
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:5000/register", this.state);

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

  render() {
    return (
      <div className="register-container">
        <h2>Register Account Holder</h2>
        <form onSubmit={this.handleSubmit} className="register-form">
          <input
            name="first_name"
            placeholder="First Name"
            onChange={this.handleChange}
            required
          />
          <input
            name="last_name"
            placeholder="Last Name"
            onChange={this.handleChange}
            required
          />
          <input
            type="date"
            name="dob"
            onChange={this.handleChange}
            required
          />
          <input
            name="address"
            placeholder="Address"
            onChange={this.handleChange}
            required
          />
          <input
            name="phone_number"
            placeholder="Phone Number"
            onChange={this.handleChange}
            required
          />
          <input
            name="email"
            placeholder="Email"
            onChange={this.handleChange}
            required
          />
          <input
            name="aadhaar_number"
            placeholder="Aadhaar Number"
            onChange={this.handleChange}
            required
          />
          <button type="submit">Register</button>
        </form>
      </div>
    );
  }
}

export default RegisterForm;
