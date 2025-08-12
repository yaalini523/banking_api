import React, { useState } from "react";
import RegisterForm from "./components/RegisterForm";
import OpenAccountForm from "./components/OpenAccountForm";
import AccountHolders from "./components/AccountHolders";
import "./App.css";
import TransferForm from "./components/TransferForm";
import CloseAccountForm from "./components/CloseAccountForm";
import AccountDetails from "./components/AccountDetails";
import AccountHolderDetails from "./components/AccountHolderDetails";


function App() {
  const [currentPage, setCurrentPage] = useState("home");
  const [viewRole, setViewRole] = useState(null); // "admin" or "customer"
  const [customerView, setCustomerView] = useState(null); // "holders" or "accounts"

  // Reset when leaving View page
  const resetView = () => {
    setViewRole(null);
    setCustomerView(null);
  };

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
          <button
            className="app-button"
            onClick={() => {
              resetView();
              setCurrentPage("view");
            }}
          >
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
          <button
            className="app-button back-button"
            onClick={() => {
              resetView();
              setCurrentPage("home");
            }}
          >
            ⬅ Back
          </button>

          {/* Select role (Admin / Customer) */}
          {!viewRole && (
            <div className="button-group">
              <button className="app-button" onClick={() => setViewRole("admin")}>
                Admin
              </button>
              <button className="app-button" onClick={() => setViewRole("customer")}>
                Customer
              </button>
            </div>
          )}

          {/* Admin view */}
          {viewRole === "admin" && <AccountHolders />}

          {/* Customer options */}
          {viewRole === "customer" && !customerView && (
            <div className="button-group">
              <button className="app-button" onClick={() => setCustomerView("holders")}>
                Account Holder
              </button>
              <button className="app-button" onClick={() => setCustomerView("accounts")}>
                Holders Account
              </button>
            </div>
          )}

          {/* Customer: Account Holders */}
          {viewRole === "customer" && customerView === "holders" && <AccountHolderDetails/>}

          {/* Customer: Accounts of that Holder (placeholder, implement your component here) */}
          {viewRole === "customer" && customerView === "accounts" && <AccountDetails/>}
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
