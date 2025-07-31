import React , { useState }from 'react';

const Customers = () => {
    <div>
      <h2>Customer Management</h2>
      <p>Here you can view and manage your customer records.</p>
      {/* Later include customer list table, search, and actions here */}
    </div>
  
  const [form, setForm] = useState({ name: '', email: '' });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Added customer: ${form.name} - ${form.email}`);
    setForm({ name: '', email: '' });
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: '2rem' }}>
        <input name="name" placeholder="Customer Name" value={form.name} onChange={handleChange} required />
        <input name="email" placeholder="Email" value={form.email} onChange={handleChange} required type="email" />
        <button type="submit">Add</button>
      </form>
      <table border="1" cellPadding="8" cellSpacing="0">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>1</td>
            <td>Shirat</td>
            <td>shirat2@gmail.com</td>
            <td><button>View</button> <button>Delete</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default Customers;