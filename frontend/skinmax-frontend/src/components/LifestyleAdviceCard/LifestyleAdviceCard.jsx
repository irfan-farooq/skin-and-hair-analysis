import "./LifestyleAdviceCard.css";

export default function LifestyleAdviceCard({
  advice = [],
}) {
  const icons = [
    "💊",
    "🍊",
    "🛏",
    "🚫",
    "💧",
    "🥗",
  ];

  return (
    <div className="lifestyle-card">
      <h3>
        🧠 Lifestyle Advice
      </h3>

      <div className="advice-grid">
        {advice.map((item, index) => (
          <div
            key={index}
            className="advice-item"
          >
            <span className="advice-icon">
              {
                icons[
                  index %
                    icons.length
                ]
              }
            </span>

            <p>{item}</p>
          </div>
        ))}
      </div>
    </div>
  );
}