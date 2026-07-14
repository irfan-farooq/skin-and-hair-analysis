import "./RoutineCard.css";

export default function RoutineCard({
  advice = {},
}) {
  const morning =
    advice?.routine_am || [];

  const evening =
    advice?.routine_pm || [];

  return (
    <div className="routine-card">

      <h4 className="routine-title">
        RECOMMENDED RITUAL
      </h4>

      <div className="routine-grid">

        <div className="routine-column">
          <h3>☀️ Morning Ritual</h3>

          {morning.length === 0 ? (
            <p>
              No morning routine available.
            </p>
          ) : (
            morning.map(
              (item, index) => (
                <div
                  key={index}
                  className="routine-item"
                >
                  <strong>
                    Step {index + 1}
                  </strong>

                  <p>{item}</p>
                </div>
              )
            )
          )}
        </div>

        <div className="routine-column">
          <h3>🌙 Evening Ritual</h3>

          {evening.length === 0 ? (
            <p>
              No evening routine available.
            </p>
          ) : (
            evening.map(
              (item, index) => (
                <div
                  key={index}
                  className="routine-item"
                >
                  <strong>
                    Step {index + 1}
                  </strong>

                  <p>{item}</p>
                </div>
              )
            )
          )}
        </div>

      </div>

    </div>
  );
}