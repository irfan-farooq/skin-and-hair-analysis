import "./AcneAnalysisCard.css";

export default function AcneAnalysisCard({
  results = {},
}) {
  const severity =
    results.acne_severity || "N/A";

  const count =
    results.acne_count ?? "N/A";

  return (
    <div className="acne-card">

      <h4 className="section-title">
        ACNE ANALYSIS
      </h4>

      <div className="zones-grid">

        <div className="zone-card red">
          <h3>Severity</h3>

          <p>{severity}</p>

          <button>
            Analysis
          </button>
        </div>

        <div className="zone-card blue">
          <h3>Detected Spots</h3>

          <p>{count}</p>

          <button>
            Review
          </button>
        </div>

      </div>

      {count === 0 && (
        <div
          style={{
            marginTop: "20px",
            padding: "16px",
            background: "#f4fdf6",
            borderRadius: "12px",
            color: "#0f7a34",
            fontWeight: "600",
          }}
        >
          ✓ No active acne detected
        </div>
      )}

    </div>
  );
}