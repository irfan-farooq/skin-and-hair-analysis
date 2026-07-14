import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar/Sidebar";
import { auth } from "../Firebase";

import "../styles/routinePage.css";

export default function RoutinePage() {
  const [routine, setRoutine] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    fetchLatestRoutine();
  }, []);

  const fetchLatestRoutine =
    async () => {
      try {
        const user =
          auth.currentUser;

        if (!user) return;

        const token =
          await user.getIdToken();

        const response =
          await fetch(
            "http://127.0.0.1:5000/api/history",
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );

        const data =
          await response.json();

        if (
          data.scans &&
          data.scans.length > 0
        ) {
          setRoutine(
            data.scans[0].advice
          );
        }
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

  const morning =
    routine?.routine_am || [];

  const evening =
    routine?.routine_pm || [];

  const lifestyle =
    routine?.lifestyle || [];

  return (
    <div className="layout">
      <Sidebar />

      <main className="routine-content">

        <div className="routine-header">
          <h1>
            Personalized Routine
          </h1>

          <p>
            Generated from your
            latest skin analysis.
          </p>
        </div>

        {loading ? (
          <p>Loading...</p>
        ) : (
          <>
            <div className="routine-grid">

              <div className="routine-card">
                <h2>
                  ☀ Morning Routine
                </h2>

                {morning.length ===
                0 ? (
                  <p>
                    No morning
                    recommendations.
                  </p>
                ) : (
                  morning.map(
                    (
                      item,
                      index
                    ) => (
                      <div
                        key={
                          index
                        }
                        className="routine-step"
                      >
                        <strong>
                          Step{" "}
                          {index +
                            1}
                        </strong>

                        <p>
                          {item}
                        </p>
                      </div>
                    )
                  )
                )}
              </div>

              <div className="routine-card">
                <h2>
                  🌙 Evening Routine
                </h2>

                {evening.length ===
                0 ? (
                  <p>
                    No evening
                    recommendations.
                  </p>
                ) : (
                  evening.map(
                    (
                      item,
                      index
                    ) => (
                      <div
                        key={
                          index
                        }
                        className="routine-step"
                      >
                        <strong>
                          Step{" "}
                          {index +
                            1}
                        </strong>

                        <p>
                          {item}
                        </p>
                      </div>
                    )
                  )
                )}
              </div>

            </div>

            <div className="tips-card">
              <h2>
                🧠 Lifestyle Advice
              </h2>

              {lifestyle.length ===
              0 ? (
                <p>
                  No lifestyle
                  advice available.
                </p>
              ) : (
                lifestyle.map(
                  (
                    item,
                    index
                  ) => (
                    <div
                      key={index}
                      className="tip-item"
                    >
                      {item}
                    </div>
                  )
                )
              )}
            </div>
          </>
        )}

      </main>
    </div>
  );
}