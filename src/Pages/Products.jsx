import React from 'react';
import { useState } from 'react';

<div>
  <h2>Product Management</h2>
   <p>Here you can add, edit, or remove products.</p>
  {/* You can later include a product list table, search bar, and form here */}
</div>


const Products = () => {
const [form, setForm] = useState({ name: ''});

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Added product: ${form.name}`);
    setForm({ name: '' });
  };

  return (
    <div>
      <h2>Product Management</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: '2rem' }}>
        <input name="name" placeholder="Product Name" value={form.name} onChange={handleChange} required />
        <button type="submit">Add</button>
      </form>
      <table border="2" cellPadding="9" cellSpacing="5">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>1</td>
            <td>LED Ceiling Light</td>
            <td><button>Edit</button> <button>Delete</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};


export default Products;
