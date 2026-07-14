import { BrowserRouter, Routes, Route } from "react-router-dom";

import LandingPage from "./pages/landingPage";
import HomePage from "./pages/homePage";
import Login from "./pages/login";
import ScanPage from "./pages/ScanPage";
import AnalysisPage from "./pages/AnalysisPage";
import DermatologistsPage from "./pages/DermatologistPage";
import WeatherPage from "./pages/WeatherPage";
import RoutinePage from "./pages/RoutinePage";
import ProgressPage from "./pages/ProgressPage";
import ChatPage from "./pages/ChatPage";


function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/"
          element={<LandingPage />}
        />

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/home"
          element={<HomePage />}
        />

        <Route
          path="/scan"
          element={<ScanPage />}
        />

        <Route
          path="/analysis"
          element={<AnalysisPage />}
        />

        <Route
          path="/dermatologists"
          element={<DermatologistsPage />}
        />

        <Route
          path="/weather"
          element={<WeatherPage />}
        />

        <Route
          path="/routines"
          element={<RoutinePage />}
        />
        <Route
          path="/progress"
          element={<ProgressPage />}
        />
        <Route
          path="/chat"
          element={<ChatPage />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;