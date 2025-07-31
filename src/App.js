import React from 'react';
import SideBar from './Components/SideBar';
import AddCustomer from './Pages/AddCustomer';
import Dashboard from './Pages/DashBoard';
import Products from './Pages/Products';
import Customers from './Pages/Customers';
import Testimonials from './Pages/Testimonials';
import Inquiries from './Pages/Inquiries';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';


function App() {
  return (
    <Router>
      <div className='d-flex'>
        <SideBar />
        <div className="flex-grow-1 p-4 bg-light min-vh-100">
          <Routes>
            <Route path="/" element={<Navigate to="/add-customer" />} />
            <Route path="/add-customer" element={<AddCustomer />} />
            <Route path="/admin" element={<Dashboard />} />
            <Route path="/admin/products" element={<Products />} />
            <Route path="/admin/customers" element={<Customers />} />
            <Route path="/admin/testimonials" element={<Testimonials />} />
            <Route path="/admin/inquiries" element={<Inquiries />} />
            
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
