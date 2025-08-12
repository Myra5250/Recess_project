import React, { useEffect, useState } from "react";
import "../styles/Home.css";
import { useNavigate } from "react-router-dom";

const heroImages = [
  "/images/hero/hero1.jpg",
  "/images/hero/hero2.jpg",
  "/images/hero/hero3.jpg",
];

const testimonials = [
  {
    text: "I’ve been shopping from CAROLINE WAYS LTD for over a year now. Their product quality is unmatched.",
    author: "— Sarah N., Interior Designer",
  },
  {
    text: "As a contractor, I rely on trusted suppliers and CAROLINE WAYS LTD never disappoints.",
    author: "— James K., Electrical Technician",
  },
];

const Home = () => {
  const [currentImage, setCurrentImage] = useState(0);
  const [products, setProducts] = useState([]);
  const [currentTestimonial, setCurrentTestimonial] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("/data/products.json")
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((err) => console.error("Failed to load products:", err));
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImage((prev) => (prev + 1) % heroImages.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTestimonial((prev) => (prev + 1) % testimonials.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleCategoryClick = (category) => {
    navigate(`/products?category=${encodeURIComponent(category)}`);
  };

  return (
    <div className="home">
      {/* Hero Section */}
      <div
        className="hero"
        style={{ backgroundImage: `url(${heroImages[currentImage]})` }}
      >
        <div className="overlay">
          <h1>QUALITY YOU CAN RELY ON</h1>
          <p>
            Supplying trusted electrical light products for homes, businesses, and contractors.
          </p>
          <button className="cta-btn" onClick={() => navigate("/products")}>
            VIEW PRODUCTS
          </button>
        </div>
      </div>

      {/* Categories Section */}
      <section className="categories">
        <h2>Our Product Categories</h2>
        <div className="category-grid">
          {[
            "Parts & Spares",
            "LED Light",
            "Pendant & Ceiling",
            "Floor Lamps",
            "Wall Lamps",
            "Table Lamps",
            "Chandeliers",
            "Fragrance Diffusers",
            "Lighting bulbs",
            "New Features",
          ].map((cat, index) => (
            <div
              className="category-card"
              key={index}
              onClick={() => handleCategoryClick(cat)}
            >
              {cat}
            </div>
          ))}
        </div>
      </section>

{/* Featured Products Section */}
<section className="featured">
  <h2>Featured Products</h2>
  <div className="product-grid">
    {products.length > 0 ? (
      products.slice(0, 6).map((product) => (
        <div className="product-card" key={product.id}>
          <img src={product.image} alt={product.name} />
          <h3>{product.name}</h3>

          <div className="product-actions">
         <button
  onClick={() => {
    const message = `Hello, I'm interested in ${product.name}.\nCheck this image: ${product.image}`;
    window.open(`https://wa.me/256753670268?text=${encodeURIComponent(message)}`, "_blank");
  }}
>
  WhatsApp
</button>

            <button onClick={() => (window.location.href = "tel:+256753670268")}>
              Call
            </button>
          </div>
        </div>
      ))
    ) : (
      <p>Loading products...</p>
    )}
  </div>
</section>

      {/* Testimonials Section */}
      <section className="testimonials">
        <h2>Testimonials</h2>
        <div className="testimonial-list">
          <blockquote key={currentTestimonial}>
            {testimonials[currentTestimonial].text}
            <footer>{testimonials[currentTestimonial].author}</footer>
          </blockquote>
        </div>
      </section>
    </div>
  );
};

export default Home;
