import React from 'react';
import { Nav } from 'react-bootstrap'
import { Link } from 'react-router-dom';

const SideBar = () => {
  return (
    <div className="bg-success text-white vh-100 p-3" style={{ width: '250px' }}>
      <h4 className="mb-4 mt-4">Admin Panel</h4>
      <nav>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li><Nav.Link as={Link} to="/admin">Dashboard</Nav.Link></li>
          <li><Nav.Link as={Link} to="/admin/products">Products</Nav.Link></li>
          <li><Nav.Link as={Link} to="/admin/customers">Customers</Nav.Link></li>
          <li><Nav.Link as={Link} to="/add-customer">Add Customer</Nav.Link></li>
          <li><Nav.Link as={Link} to="/admin/inquiries">Inquiries</Nav.Link></li>
          <li><Nav.Link as={Link} to="/admin/testimonials">Testimonials</Nav.Link></li>
          
        </ul>
      </nav>
    </div>
  );
};

export default SideBar;

