import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
// import { CartProvider } from './context/CartContext';  // Removed since CartContext deleted
import "./styles/App.css";
import "./index.css";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <BrowserRouter>

    <App />
  </BrowserRouter>
);
