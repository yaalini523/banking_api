import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:5000",
});

export const registerHolder = (data) => API.post("/register", data);
export const openAccount = (data) => API.post("/open_account", data);
export const getAllHolders = () =>
  API.get("/account_holders", {
    headers: {
      Role: "Admin",
    },
  });
export const transferFunds = (data) => API.post("/transfer", data);
export const closeAccount = (id) => API.delete(`/close_account/${id}`);
