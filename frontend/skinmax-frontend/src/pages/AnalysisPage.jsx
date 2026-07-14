import Sidebar from "../components/Sidebar/Sidebar";

import OverviewCard from "../components/OverviewCard/OverviewCard";
import SkinProfileCard from "../components/SkinProfileCard/SkinProfileCard";
import AcneAnalysisCard from "../components/AcneAnalysisCard/AcneAnalysisCard";
import RoutineCard from "../components/RoutineCard/RoutineCard";
import LifestyleAdviceCard from "../components/LifestyleAdviceCard/LifestyleAdviceCard";

import "../styles/analysis.css";

export default function AnalysisPage() {
  const uploadedImage =
    localStorage.getItem("uploadedImage");

  const analysisData = JSON.parse(
    localStorage.getItem("analysisResults")
  );

  const results =
    analysisData?.results || {};

  const advice =
    results?.advice || {};

  return (
    <div className="layout">
      <Sidebar />

      <main className="content">
        <div className="dashboard-container">

          <header className="page-header">
            <h1>Skin Analysis Report</h1>

            <p>
              AI-powered assessment of your
              uploaded facial image.
            </p>
          </header>

          <OverviewCard
            image={uploadedImage}
            results={results}
          />

          <SkinProfileCard
            results={results}
          />

          <AcneAnalysisCard
            results={results}
          />

          <RoutineCard
            advice={advice}
          />
          <LifestyleAdviceCard
            advice={
              results?.advice?.lifestyle || []
            }
          />

        </div>
      </main>
    </div>
  );
}