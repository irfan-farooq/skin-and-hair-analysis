import "../styles/landingPage.css";
import heroImage from "../assets/hero.jpg";
import { useNavigate } from "react-router-dom";

export default function LandingPage() {

  const navigate = useNavigate();

  return (
    <section
      className="hero-section"
      style={{
        backgroundImage: `url(${heroImage})`,
      }}
    >
      <div className="hero-overlay"></div>

      <div className="hero-logo">
        <h1>SKINMAX</h1>
      </div>

      <div className="hero-content">
        <h1 className="hero-title">
          Your glow,
          <br />
          curated.
        </h1>

        <p className="hero-subtitle">
          Curated skincare AI recommendations for clean,
          clear skin.
        </p>

        <button
          className="hero-btn"
          onClick={() => navigate("/home")}
        >
          ANALYZE TODAY
        </button>
      </div>
    </section>
  );
}