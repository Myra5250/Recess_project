import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import About from './pages/About';
import Products from './pages/Products';
import FAQ from './pages/FAQ';
import PrivacyPolicy from "./components/PrivacyPolicy";
import Contact from './pages/Contact';




function App() {
  return (
    <>
      <Navbar />
      <div className="main-content">
        <Routes>

          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/products" element={<Products />} />
          <Route path="/faq" element={<FAQ />} />
          <Route path="/privacypolicy" element={<PrivacyPolicy />} />
          <Route path="/contact" element={<Contact />} />
       
     
        </Routes>
      </div>
      <Footer />
     
    </>
  );
}

export default App;
