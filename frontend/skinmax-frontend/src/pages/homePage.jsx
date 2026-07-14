import "../styles/homePage.css";
import modelImage from "../assets/model.jpg";
import { useNavigate } from "react-router-dom";
import { logoutUser } from "../Firebase";
import { auth } from "../Firebase";
window.getToken = async () => {
  console.log(
    await auth.currentUser.getIdToken()
  );
};


export default function HomePage() {
  const navigate = useNavigate();

  const isLoggedIn =
    localStorage.getItem("isLoggedIn");

  const user = JSON.parse(
    localStorage.getItem("user")
  );

  const handleAnalysis = () => {
    if (isLoggedIn) {
      navigate("/scan");
    } else {
      localStorage.setItem(
        "redirectAfterLogin",
        "/scan"
      );

      navigate("/login");
    }
  };

  const handleProtectedNavigation = (
    path
  ) => {
    if (isLoggedIn) {
      navigate(path);
    } else {
      localStorage.setItem(
        "redirectAfterLogin",
        path
      );

      navigate("/login");
    }
  };
  

  const handleLogout = async () => {
    try {
      await logoutUser();

      localStorage.removeItem(
        "isLoggedIn"
      );

      localStorage.removeItem(
        "user"
      );

      localStorage.removeItem(
        "redirectAfterLogin"
      );

      navigate("/home");

      window.location.reload();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="home-page">
      <header className="navbar">
        <div className="logo">SkinMax</div>

        <nav>
          <button
            className="nav-link"
            onClick={handleAnalysis}
          >
            Analysis
          </button>

          <button
            className="nav-link"
            onClick={() =>
              handleProtectedNavigation(
                "/routines"
              )
            }
          >
            Routines
          </button>

          <button
            className="nav-link"
            onClick={() =>
              handleProtectedNavigation(
                "/progress"
              )
            }
          >
            Progress
          </button>

          <button
            className="nav-link"
            onClick={() =>
              handleProtectedNavigation(
                "/weather"
              )
            }
          >
            Weather Care
          </button>
        </nav>

        <div className="actions">
          {isLoggedIn ? (
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "12px",
              }}
            >
              {user?.photoURL ? (
                <img
                  src={user.photoURL}
                  alt="Profile"
                  style={{
                    width: "40px",
                    height: "40px",
                    borderRadius: "50%",
                    objectFit: "cover",
                  }}
                />
              ) : (
                <div
                  style={{
                    width: "40px",
                    height: "40px",
                    borderRadius: "50%",
                    background: "#e6c3aa",
                  }}
                />
              )}

              <span
                style={{
                  fontWeight: "600",
                  color: "#111",
                }}
              >
                {user?.displayName}
              </span>

              <button
                className="login-btn"
                onClick={handleLogout}
              >
                Logout
              </button>
            </div>
          ) : (
            <>
              <button
                className="login-btn"
                onClick={() => navigate("/login")}
              >
                Log In
              </button>

              <button
                className="signup-btn"
                onClick={() => navigate("/login")}
              >
                Sign Up
              </button>
            </>
          )}
        </div>
      </header>

      <section className="hero">
        <div className="blob blob1"></div>
        <div className="blob blob2"></div>

        <span className="badge">
          PIONEERING COMPUTER VISION
        </span>

        <h1>
          Discover Your Best Skin
          <br />
          with AI
        </h1>

        <p>
          Advanced facial analysis powered by
          computer vision and artificial
          intelligence. Personalized clinical
          precision in the comfort of your own
          home.
        </p>

        <div className="hero-buttons">
          <button
            className="primary-btn"
            onClick={handleAnalysis}
          >
            Start Your Analysis
          </button>

          <button
            className="secondary-btn"
            onClick={() =>
              handleProtectedNavigation(
                "/analysis"
              )
            }
          >
            View Sample Report
          </button>
        </div>

        <div className="hero-card">
          <img src={modelImage} alt="AI Analysis" />

          <div className="floating-card hydration">
            <h4>Hydration Level</h4>

            <div className="bar">
              <div className="fill"></div>
            </div>

            <span>82% Optimal</span>
          </div>

          <div className="floating-card recommendation">
            <h4>AI Recommendation</h4>

            <p>
              Switch to a ceramide-based
              cleanser for nightly repair.
            </p>
          </div>
        </div>
      </section>

      <section className="features">
        <h2>Precision Met with Ritual</h2>

        <p>
          Beyond surface level. We analyze
          multiple markers to curate your
          routine.
        </p>

        <div className="bento-grid">
          <div className="card large">
            <h3>Precision Analysis</h3>

            <p>
              AI-powered skin diagnostics
              with detailed insights.
            </p>
          </div>

          <div className="card tall">
            <h3>Progress Tracking</h3>

            <p>
              Track improvements across
              weeks and months.
            </p>
          </div>

          <div className="card">
            <h3>AI Chat</h3>

            <p>
              Ask questions about your
              routine in real time.
            </p>
          </div>

          <div className="card wide">
            <h3>Custom Routines</h3>

            <p>
              Morning and evening protocols
              tailored for your skin.
            </p>
          </div>
        </div>
      </section>

      <section className="flow">
        <h2>The Ritual Flow</h2>

        <div className="steps">
          <div className="step">
            <span>01</span>
            <h3>Snap a Selfie</h3>
          </div>

          <div className="step">
            <span>02</span>
            <h3>AI Processing</h3>
          </div>

          <div className="step">
            <span>03</span>
            <h3>Daily Protocol</h3>
          </div>
        </div>
      </section>

      <section className="testimonials">
        <h2>Voices of Clarity</h2>

        <div className="testimonial-grid">
          <div className="testimonial">
            <p>
              "The AI analysis was startlingly
              accurate."
            </p>

            <h4>Elena R.</h4>
          </div>

          <div className="testimonial">
            <p>
              "My routine is now minimal and
              effective."
            </p>

            <h4>Marcus T.</h4>
          </div>
        </div>
      </section>

      <section className="cta">
        <h2>
          Ready for Your Private
          Consultation?
        </h2>

        <p>
          Start your first scan today and
          experience the future of skincare.
        </p>

        <button
          className="primary-btn"
          onClick={handleAnalysis}
        >
          Start Your Analysis
        </button>
      </section>

      <footer className="footer">
        <div>
          <h3>SkinMax</h3>
          <p>© 2026 SkinMax</p>
        </div>

        <div className="footer-links">
          <a href="#">Privacy Policy</a>
          <a href="#">Terms of Service</a>
          <a href="#">Contact</a>
        </div>
      </footer>
    </div>
  );
}