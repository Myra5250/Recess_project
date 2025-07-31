import React, {useState} from 'react';

const Testimonials = () => {
    const [form, setform] = useState ({message: '' });
    const [testimonials , setTestimonials] = useState([]);
    
    const handleChange = (e) => {
        setform({ ...form, [e.target.name]: e.target.value});
    };
    
        const handleSubmit = (e) => {
            e.preventDefault();
            const newTestimonial = {id: testimonials.length + 1, ...form };
            setTestimonials([...testimonials, newTestimonial]);
            setform ({ name: '', comment: '' });
    }
       
    return (
        <div>
            <h2>Customer Testimonials</h2>
            <form onSubmit={handleSubmit} style={{marginBottom: '2rem' }}>
                <input name="name" placeholder= "Customer Name" value={form.name} onChange={handleChange} required />
                <textarea name="comment" placeholder="Testimonial" value={form.name} onChange={handleChange} required/>
                <button type="submit">Add</button>
            </form>
            <ul>
                {testimonials.map((t) => (
                    <li key={t.id}><strong>{t.name}</strong>: {t.comment}</li>
                ))}
            </ul>
        </div>
      );
    };
    
export default Testimonials;