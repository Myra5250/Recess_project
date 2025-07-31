import React, {useState} from 'react';

const Inquiries = () => {
  const [form, setForm] = useState({ message: '' });
  const [inquiries, setInquiries] = useState([]);

  const handleChange = (e) => setForm({ message: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();
    const newInquiry = { id: inquiries.length + 1, ...form };
    setInquiries([...inquiries, newInquiry]);
    setForm({ message: '' });
  };

  return (
    <div>
      <h2>Customer Inquiries</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: '1rem' }}>
        <textarea placeholder="Enter inquiry" value={form.message} onChange={handleChange} required />
        <button type="submit">Submit</button>
      </form>
      <ul>
        {inquiries.map((inq) => (
          <li key={inq.id}>{inq.message}</li>
        ))}
      </ul>
    </div>
  );
};

export default Inquiries;
