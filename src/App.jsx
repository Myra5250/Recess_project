import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AdminLayout from './Layouts/AdminLayout';
import Dashboard from './Pages/DashBoard';
import Products from './Pages/Products';
import AddCustomer from './Pages/AddCustomer';
import Testimonials from './Pages/Testimonials';
import Customers from './Pages/Customers';
import Inquiries from './Pages/Inquiries';


const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/admin" element={<AdminLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="products" element={<Products />} />
          <Route path="add-customer" element={<AddCustomer />} />
          <Route path="testimonials" element={<Testimonials />} />
          <Route path="customers" element={<Customers />} />
          <Route path="inquiries" element={<Inquiries />} />
          {/* You can add more nested routes here for products, customers, etc. */}
        </Route>
      </Routes>
    </Router>
  );
};

export default App;