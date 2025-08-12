import React from 'react';
import '../styles/Contact.css';

const Contact = () => {
  return (
    <div className="contact-container">
      <h2>Contact Us</h2>

      <div className="contact-info">
        <div className="map">
          <iframe
            title="Caroline Ways Ltd Location"
            src="https://www.google.com/maps?q=Market+Street+Energy+Center+H1-44+Kampala+Uganda&output=embed"
            width="100%"
            height="300"
            style={{ border: 0 }}
            allowFullScreen=""
            loading="lazy"
          ></iframe>
        </div>

        <div className="details">
          <p><strong>Address:</strong> Caroline Ways Limited, Market Street Energy Center H1-44, P.O. Box 4143, Kampala, Uganda</p>
          <p><strong>Phone:</strong> 0774433927, 0754433927, 0752950250, 0707280933</p>
          <p><strong>Email:</strong> info@carolineways.com</p>
          <p><strong>Note:</strong> <em>Goods once sold are not returnable.</em></p>
        </div>
      </div>

      <form className="contact-form">
        <h3>Send Us a Message</h3>
        <input type="text" placeholder="Your Name" required />
        <input type="email" placeholder="Your Email" required />
        <textarea rows="5" placeholder="Your Message" required></textarea>
        <button type="submit">Send Message</button>
      </form>
    </div>
  );
};

export default Contact;
