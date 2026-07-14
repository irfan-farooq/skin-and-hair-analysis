import { useNavigate } from "react-router-dom";
import { loginWithGoogle } from "../firebase";
import "../styles/login.css";

export default function Login() {
  const navigate = useNavigate();

  const handleGoogleLogin = async () => {
    try {
      const data = await loginWithGoogle();
      localStorage.setItem(
        "token",
        data.token
      );
      
      localStorage.setItem(
        "user",
        JSON.stringify(data.user)
      );

      localStorage.setItem(
        "isLoggedIn",
        "true"
      );

      const redirectAfterLogin =
        localStorage.getItem(
          "redirectAfterLogin"
        );

      if (redirectAfterLogin) {
        localStorage.removeItem(
          "redirectAfterLogin"
        );

        navigate(redirectAfterLogin);
      } else {
        navigate("/home");
      }
    } catch (error) {
      console.error(error);

      alert("Google Sign In failed");
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">

        <div className="login-header">
          <h1>SkinMax</h1>
          <p>AI SKINCARE RITUAL</p>
        </div>

        <button
          className="google-btn"
          onClick={handleGoogleLogin}
        >
          <img
            src="https://developers.google.com/identity/images/g-logo.png"
            alt="Google"
            style={{
              width: "20px",
              height: "20px",
              marginRight: "12px"
            }}
          />

          Continue with Google
        </button>

        <p
          style={{
            marginTop: "24px",
            color: "#777",
            fontSize: "14px",
            textAlign: "center"
          }}
        >
          Secure authentication powered by Google
        </p>

      </div>

      <footer className="login-footer">
        <div className="footer-links">
          <a href="#">Privacy</a>
          <a href="#">Terms</a>
          <a href="#">Sustainability</a>
        </div>

        <p>
          © 2026 SkinMax. Premium AI Skincare.
        </p>
      </footer>
    </div>
  );
}