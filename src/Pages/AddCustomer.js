import { Form, Button, Alert } from 'react-bootstrap';
import { useState } from 'react';
import axios from 'axios';

const AddCustomer = () => {
  const [form, setForm] = useState({
    name: '',
    email: '',
    address: '',
    phone: '',
    password: '',
  });

  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Sending form data:', form);  // Optional: for debugging
    try {
      // ✅ Corrected URL
      await axios.post('http://127.0.0.1:5000/api/v1/customer/register', form);

      setMessage('Customer added successfully!');
      setForm({
        name: '',
        email: '',
        address: '',
        phone: '',
        password: '',
      });
    } catch (err) {
      console.error('Error adding Customer:', err);
      let errorMsg = 'Error adding Customer';
      if (err.response && err.response.data) {
        errorMsg = err.response.data.message || JSON.stringify(err.response.data);
      } else if (err.message) {
        errorMsg = err.message;
      }
      setMessage(errorMsg);
    }
  };

  return (
    <div className="p-4">
      <h4>Add Customer</h4>

      {message && <Alert variant="info">{message}</Alert>}

      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Name</Form.Label>
          <Form.Control
            type="text"
            name="name"
            value={form.name}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Phone Number</Form.Label>
          <Form.Control
            type="tel"
            name="phone"
            value={form.phone}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Email</Form.Label>
          <Form.Control
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            name="password"
            value={form.password}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Button type="submit" variant="primary">
          Add Customer
        </Button>
      </Form>
    </div>
  );
};

export default AddCustomer;