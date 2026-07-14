import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar/Sidebar";
import { auth } from "../Firebase";

import "../styles/ProgressPage.css";

export default function ProgressPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
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

      setHistory(
        data.scans || []
      );
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const latest =
    history.length > 0
      ? history[0]
      : null;

  return (
    <div className="layout">
      <Sidebar />

      <main className="progress-content">

        <div className="progress-header">
          <h1>
            Progress Tracker
          </h1>

          <p>
            Monitor your skin
            journey over time.
          </p>
        </div>

        <div className="stats-grid">

          <div className="stat-card">
            <h3>Total Scans</h3>

            <div className="stat-value">
              {history.length}
            </div>
          </div>

          <div className="stat-card">
            <h3>
              Current Acne
            </h3>

            <div className="stat-value">
              {
                latest?.acne_severity ||
                "-"
              }
            </div>
          </div>

          <div className="stat-card">
            <h3>
              Skin Tone
            </h3>

            <div className="stat-value">
              {latest?.skin_tone || "-"}
            </div>
          </div>

        </div>

        <div className="history-card">

          <h2>Scan History</h2>

          {loading && (
            <p>Loading...</p>
          )}

          {!loading &&
            history.length === 0 && (
              <p>
                No scans found.
              </p>
            )}

          {history.map(
            (scan) => (
              <div
                key={scan.scan_id}
                className="history-item"
              >
                <div>
                  📅{" "}
                  {new Date(
                    scan.created_at
                  ).toLocaleDateString()}
                </div>

                <div>
                  Skin Tone:{" "}
                  {
                    scan.skin_tone
                  }
                </div>

                <div>
                  Acne:{" "}
                  {
                    scan.acne_severity
                  }
                </div>

                <div>
                  Face Shape:{" "}
                  {
                    scan.face_shape
                  }
                </div>
              </div>
            )
          )}
        </div>

      </main>
    </div>
  );
}