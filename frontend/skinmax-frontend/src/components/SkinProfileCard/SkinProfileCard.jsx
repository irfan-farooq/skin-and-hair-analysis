import "./SkinProfileCard.css";

export default function SkinProfileCard({
  results = {},
}) {
  return (
    <div className="skin-profile-card">

      <h4 className="section-title">
        SKIN PROFILE
      </h4>

      <div className="profile-grid">

        <div className="profile-item">
          <span>Skin Tone</span>
          <strong>
            {results.skin_tone || "N/A"}
          </strong>
        </div>

        <div className="profile-item">
          <span>Undertone</span>
          <strong>
            {results.undertone || "N/A"}
          </strong>
        </div>

        <div className="profile-item">
          <span>Face Shape</span>
          <strong>
            {results.face_shape || "N/A"}
          </strong>
        </div>

        <div className="profile-item">
          <span>Eye Color</span>
          <strong>
            {results.eye_color || "N/A"}
          </strong>
        </div>

        <div className="profile-item">
          <span>Hair Type</span>
          <strong>
            {results.hair_type || "N/A"}
          </strong>
        </div>

        <div className="profile-item">
          <span>Dark Circles</span>
          <strong>
            {results.dark_circles || "N/A"}
          </strong>
        </div>

      </div>
    </div>
  );
}