import "./OverviewCard.css";

import hero from "../../assets/sample-image.jpg";
import FaceViewer from "../FaceHeatmap/FaceViewer";

export default function OverviewCard({
  image,
  results = {},
}) {
  return (
    <div className="overview-card">

  <div className="overview-left">

    <h3>Original Scan</h3>

    <div className="image-wrapper">
      <img
        src={image || hero}
        alt="Original Face Scan"
      />
    </div>

  </div>

  <div className="overview-right">

    <h3>AI Analysis</h3>

    <div className="viewer-wrapper">
      <FaceViewer
        detections={
          results.acne_detections || []
        }
      />
    </div>

  </div>

</div>
  );
}