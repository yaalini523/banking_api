import axios from "axios"; //HTTP client library for making requests (GET, POST, DELETE, etc.) to APIs.

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5001";

const bankapi = axios.create({
  baseURL: API_URL,
});

export const registerHolder = (data) => bankapi.post("/register", data);
export const openAccount = (data) => bankapi.post("/open_account", data);
export const getAllHolders = (authRole) =>
  bankapi.get("/account_holders", {
    headers: {
      AuthRole: authRole,
    },
  });
export const getHolderInfo = (phone) =>
  bankapi.get("/get_holder_info", { params: { phone, type: "details" } });
export const getAccountsByHolder = (holderId) =>
  bankapi.get(`/get_accounts_by_holder/${holderId}`);
export const transferFunds = (data) => bankapi.post("/transfer", data);
export const closeAccount = (id) => bankapi.delete(`/close_account/${id}`);

export default bankapi;
