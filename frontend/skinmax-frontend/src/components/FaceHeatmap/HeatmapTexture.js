import * as THREE from "three";

export function createHeatmapTexture(points = []) {
  const size = 2048;

  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;

  const ctx = canvas.getContext("2d");

  // transparent background
  ctx.clearRect(0, 0, size, size);

  points.forEach((p) => {
    const x = p.u * size;
    const y = (1 - p.v) * size;

    const radius = p.radius || 20;

    // create multiple overlapping blobs
    for (let i = 0; i < 5; i++) {
      const dx = (Math.random() - 0.5) * radius * 0.6;
      const dy = (Math.random() - 0.5) * radius * 0.6;

      const gradient = ctx.createRadialGradient(
        x + dx,
        y + dy,
        0,
        x + dx,
        y + dy,
        radius
      );

      gradient.addColorStop(0.00, "rgba(255,0,0,0.20)");
      gradient.addColorStop(0.20, "rgba(255,80,0,0.12)");
      gradient.addColorStop(0.50, "rgba(255,160,0,0.06)");
      gradient.addColorStop(1.00, "rgba(255,160,0,0)");

      ctx.fillStyle = gradient;

      ctx.beginPath();
      ctx.arc(x + dx, y + dy, radius, 0, Math.PI * 2);
      ctx.fill();
    }
  });

  const texture = new THREE.CanvasTexture(canvas);

  texture.flipY = false;
  texture.needsUpdate = true;

  return texture;
}