import { useState, useEffect, useCallback } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";
import AetherNetDashboard from "@/components/AetherNetDashboard";
import StockMarketDashboard from "@/components/StockMarketDashboard";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AetherNetDashboard api={API} />} />
          <Route path="/market" element={<StockMarketDashboard api={API} />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;