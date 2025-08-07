import React, { useState } from "react";
import RegisterForm from "./components/RegisterForm";
import OpenAccountForm from "./components/OpenAccountForm";
import AccountHolders from "./components/AccountHolders";
import "./App.css";
import TransferForm from "./components/TransferForm";
import CloseAccountForm from "./components/CloseAccountForm";

function App() {
  const [currentPage, setCurrentPage] = useState("home");

  return (
    <div className="app-container">
      <h1 className="app-title">Banking Dashboard</h1>

      {currentPage === "home" && (
        <div className="button-group">
          <button className="app-button" onClick={() => setCurrentPage("register")}>
            Register Account Holder
          </button>
          <button className="app-button" onClick={() => setCurrentPage("open")}>
            Open Bank Account
          </button>
          <button className="app-button" onClick={() => setCurrentPage("view")}>
            View Account Holders
          </button>
          <button className="app-button" onClick={() => setCurrentPage("transfer")}>
            Transfer Amount
          </button>
          <button className="app-button" onClick={() => setCurrentPage("cancel")}>
            Cancel Account
          </button>
        </div>
      )}

      {currentPage === "register" && (
        <>
          <button className="app-button back-button" onClick={() => setCurrentPage("home")}>
            ⬅ Back
          </button>
          <RegisterForm />
        </>
      )}

      {currentPage === "open" && (
        <>
          <button className="app-button back-button" onClick={() => setCurrentPage("home")}>
            ⬅ Back
          </button>
          <OpenAccountForm />
        </>
      )}

      {currentPage === "view" && (
        <>
          <button className="app-button back-button" onClick={() => setCurrentPage("home")}>
            ⬅ Back
          </button>
          <AccountHolders />
        </>
      )}

      {currentPage === "transfer" && (
        <>
          <button className="app-button back-button" onClick={() => setCurrentPage("home")}>
            ⬅ Back
          </button>
          <TransferForm />
        </>
      )}

      {currentPage === "cancel" && (
        <>
          <button className="app-button back-button" onClick={() => setCurrentPage("home")}>
            ⬅ Back
          </button>
          <CloseAccountForm />
        </>
      )}

    </div>
  );
}

export default App;
