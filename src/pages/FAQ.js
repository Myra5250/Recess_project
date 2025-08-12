import React from 'react';
import '../styles/FAQ.css';

const FAQ = () => {
  return (
    <div className="faq">
      <h2>Frequently Asked Questions</h2>

      <div className="faq-item">
        <h4>What products do you offer?</h4>
        <p>We specialize in electronic light accessories including bulbs, LED strips, lamp holders, chandeliers, and more.</p>
      </div>

      <div className="faq-item">
        <h4>Can I buy directly from the website?</h4>
        <p>Currently, our website is for product display only. To place an order, please contact us via WhatsApp, phone, or email.</p>
      </div>

      <div className="faq-item">
        <h4>How do I inquire about prices or availability?</h4>
        <p>You can click on the contact buttons provided under each product or visit our <strong>Contact Us</strong> page to reach out directly.</p>
      </div>

      <div className="faq-item">
        <h4>Do you offer delivery?</h4>
        <p>Yes, we provide delivery services within Kampala and surrounding areas. Delivery fees depend on the location and product type.</p>
      </div>

      <div className="faq-item">
        <h4>Can I visit your physical store?</h4>
        <p>Yes, we have a physical shop in Kampala. Please check our contact page for directions.</p>
      </div>
    </div>
  );
};

export default FAQ;
