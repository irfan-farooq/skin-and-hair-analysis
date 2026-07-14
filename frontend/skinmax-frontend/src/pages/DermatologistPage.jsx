import { useState } from "react";
import Sidebar from "../components/Sidebar/Sidebar";

export default function DermatologistsPage() {
  const [loading, setLoading] = useState(false);

  const findDermatologists = () => {
    setLoading(true);

    if (!navigator.geolocation) {
      window.open(
        "https://www.google.com/maps/search/dermatologist+near+me",
        "_blank"
      );

      setLoading(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } =
          position.coords;

        const url =
          `https://www.google.com/maps/search/dermatologist/@${latitude},${longitude},14z`;

        window.open(url, "_blank");

        setLoading(false);
      },

      () => {
        window.open(
          "https://www.google.com/maps/search/dermatologist+near+me",
          "_blank"
        );

        setLoading(false);
      }
    );
  };

  return (
    <div className="layout">
      <Sidebar />

      <main
        style={{
          flex: 1,
          padding: "40px",
          background: "#f8f6f3",
          minHeight: "100vh",
        }}
      >
        <div
          style={{
            maxWidth: "900px",
            margin: "0 auto",
          }}
        >
          <h1
            style={{
              fontSize: "42px",
              marginBottom: "16px",
            }}
          >
            Find Dermatologists
          </h1>

          <p
            style={{
              color: "#666",
              fontSize: "18px",
              marginBottom: "40px",
            }}
          >
            Connect with qualified dermatologists
            near your location for professional
            consultation and treatment.
          </p>

          <div
            style={{
              background: "#fff",
              borderRadius: "30px",
              padding: "50px",
              boxShadow:
                "0 10px 30px rgba(0,0,0,0.05)",
              textAlign: "center",
            }}
          >
            <div
              style={{
                fontSize: "80px",
                marginBottom: "20px",
              }}
            >
              🩺
            </div>

            <h2
              style={{
                marginBottom: "16px",
              }}
            >
              Locate Nearby Dermatologists
            </h2>

            <p
              style={{
                color: "#777",
                marginBottom: "30px",
              }}
            >
              We'll use your current location
              to find dermatologists nearby
              using Google Maps.
            </p>

            <button
              onClick={findDermatologists}
              disabled={loading}
              style={{
                background: "#e6c3aa",
                border: "none",
                padding: "16px 32px",
                borderRadius: "999px",
                cursor: "pointer",
                fontSize: "16px",
                fontWeight: "600",
              }}
            >
              {loading
                ? "Finding Doctors..."
                : "Find Dermatologists Near Me"}
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}