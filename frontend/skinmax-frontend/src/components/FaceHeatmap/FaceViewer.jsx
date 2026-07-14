import { Canvas } from "@react-three/fiber";
import {
  OrbitControls,
  useGLTF,
  Center,
  Html,
} from "@react-three/drei";

function FaceModel() {
  const { scene } = useGLTF("/face.glb");

  return (
    <Center>
      <primitive
        object={scene}
        scale={1}
      />
    </Center>
  );
}

function AcneMarker({
  position,
}) {
  return (
    <Html position={position}>
      <div
        style={{
          width: "16px",
          height: "16px",
          borderRadius: "50%",
          background: "red",
          boxShadow:
            "0 0 20px red",
          transform:
            "translate(-50%, -50%)",
        }}
      />
    </Html>
  );
}

export default function FaceViewer({
  detections = [],
}) {
  const markers = detections.map(
    (d, index) => {
      const x =
        (d?.bbox?.center_x - 0.5) *
        2.5;

      const y =
        (0.5 -
          d?.bbox?.center_y) *
        3;

      return (
        <AcneMarker
          key={index}
          position={[x, y, 1]}
        />
      );
    }
  );

  return (
    <Canvas
      camera={{
        position: [0, 0, 5],
        fov: 40,
      }}
      style={{
        width: "100%",
        height: "100%",
        background: "#07122b",
      }}
    >
      <ambientLight intensity={2} />

      <directionalLight
        position={[5, 5, 5]}
        intensity={3}
      />

      <directionalLight
        position={[-5, 5, 5]}
        intensity={2}
      />

      <FaceModel />

      {markers}

      <OrbitControls
        enablePan={false}
        enableZoom={false}
        enableRotate={false}
      />
    </Canvas>
  );
}