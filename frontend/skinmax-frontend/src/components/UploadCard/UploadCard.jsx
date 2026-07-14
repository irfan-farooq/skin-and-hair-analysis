import "./UploadCard.css";

export default function UploadCard({
  image,
  setImage,
}) {
  const handleUpload = (e) => {
    const file = e.target.files[0];

    if (!file) return;

    setImage({
      file,
      preview:
        URL.createObjectURL(file),
    });
  };

  return (
    <div className="upload-card">
      <div className="upload-icon">
        ☁
      </div>

      <h3>Upload Image</h3>

      <p>
        Drag and drop your
        high-resolution skin profile
        image.
      </p>

      <div className="file-types">
        <span>JPG</span>
        <span>PNG</span>
        <span>HEIC</span>
      </div>

      <label className="upload-btn">
        Choose Image

        <input
          type="file"
          accept="image/*"
          onChange={handleUpload}
          hidden
        />
      </label>
    </div>
  );
}