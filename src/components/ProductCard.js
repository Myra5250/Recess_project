import React from "react";
import "../styles/ProductCard.css";

const ProductCard = ({ product }) => {
  const phone = "256753670268"; // Seller's WhatsApp & call number

  const handleWhatsApp = () => {
    const message = `Hello, I'm interested in ${product.name}.\nCheck this image: ${product.image}`;
    window.open(`https://wa.me/${phone}?text=${encodeURIComponent(message)}`, "_blank");
  };

  const handleCall = () => {
    window.open(`tel:+${phone}`, "_self");
  };

  return (
    <div className="product-card">
      <div className="image-wrapper">
        <img src={product.image} alt={product.name} />
      </div>
      <h3>{product.name}</h3>

      <div className="contact-buttons">
        <button className="btn contact-btn" onClick={handleWhatsApp}>
          WhatsApp
        </button>
        <button className="btn contact-btn" onClick={handleCall}>
          Call
        </button>
      </div>
    </div>
  );
};

export default ProductCard;
