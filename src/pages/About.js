import React from 'react';
import '../styles/About.css';

const About = () => {
  return (
    <div className="about-container">
      <section className="about-hero">
        <h1>About Caroline Ways Ltd</h1>
        <p>
          Caroline Ways Ltd is a leading Ugandan retailer and wholesaler specializing in high-quality electrical products. 
          Since our founding in 2019, we have committed ourselves to delivering reliable, affordable, and innovative electrical solutions 
          that empower homes, businesses, and contractors across Uganda.
        </p>
      </section>

      <section className="about-content">
        <h2>Our Story</h2>
        <p>
          Founded with a vision to bridge the gap between quality electrical supplies and affordability, Caroline Ways Ltd has grown steadily 
          to become a trusted supplier known for exceptional customer service and product reliability. Our journey started from a small shop 
          at Energy Center, Kampala, and today we serve a diverse clientele ranging from individual homeowners to large-scale commercial clients.
        </p>
        <p>
          At the core of our operations lies a dedication to sourcing the best products from reputable manufacturers and offering a wide range 
          of lighting accessories, electrical parts, and fragrance diffusers — all tailored to meet the unique needs of our customers.
        </p>

        <h2>Our Vision</h2>
        <p>
          To be the foremost provider of innovative and sustainable electrical solutions in Uganda, recognized for exceptional quality, customer satisfaction, and community impact.
        </p>

        <h2>Our Mission</h2>
        <p>
          To supply reliable and affordable electrical products that enhance the safety, comfort, and efficiency of homes and businesses, while fostering lasting relationships with our customers and partners through trust and excellence.
        </p>

        <h2>What We Offer</h2>
        <ul>
          <li>High-quality LED lights and lamps that blend functionality with aesthetics</li>
          <li>Durable parts and spares to keep your electrical installations running smoothly</li>
          <li>Innovative fragrance diffusers to enhance your living and working spaces</li>
          <li>Exceptional customer support that guides you through every purchase</li>
        </ul>

        <h2>Our Team</h2>
        <div className="team-grid">
          <div className="team-member">
            <img src="/images/products/CEO.jpg" alt="Nakalya Caroline." />
            <h3>Nakalya Caroline</h3>
            <p>Founder & CEO</p>
          </div>
          <div className="team-member">
            <img src="/images/products/confident-business-woman-portrait-smiling-face.jpg" alt="James K." />
            <h3>Justin K.</h3>
            <p>Head of Operations</p>
          </div>
          <div className="team-member">
            <img src="/images/products/person.avif" alt="Emma T." />
            <h3>Emma T.</h3>
            <p>Customer Relations Manager</p>
          </div>
          <div className="team-member">
            <img src="/images/products/person2.avif" alt="Michael B." />
            <h3>Michael B.</h3>
            <p>Product Specialist</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;
