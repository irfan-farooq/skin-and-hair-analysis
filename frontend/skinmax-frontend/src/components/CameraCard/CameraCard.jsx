import "./CameraCard.css";

export default function CameraCard({ image }) {
  return (
    <div className="camera-card">
      <img
        src={
          image?.preview
            ? image.preview
            : "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=800"
        }
        alt="Preview"
        className="camera-image"
      />

      <div className="camera-content">
        <div
          className={`camera-status ${
            image?.preview
              ? "uploaded-status"
              : ""
          }`}
        >
          {image?.preview
            ? "✓ IMAGE UPLOADED"
            : "● AI READY"}
        </div>

        <h3>
          {image?.preview
            ? "Ready For Analysis"
            : "Upload Face Image"}
        </h3>

        <p>
          {image?.preview
            ? "Your image has been uploaded successfully. Click Analyze My Skin to continue."
            : "Upload a clear front-facing image for accurate AI skin analysis."}
        </p>
      </div>
    </div>
  );
}