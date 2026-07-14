import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar/Sidebar";
import "../styles/weatherPage.css";

export default function WeatherPage() {
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(true);

  const API_KEY =
    import.meta.env.VITE_WEATHER_API_KEY;

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        try {
          const { latitude, longitude } =
            position.coords;

          const response = await fetch(
            `https://api.weatherapi.com/v1/current.json?key=${API_KEY}&q=${latitude},${longitude}&aqi=yes`
          );

          const data = await response.json();

          setWeather(data);
        } catch (error) {
          console.error(error);
        } finally {
          setLoading(false);
        }
      },

      (error) => {
        console.error(error);
        setLoading(false);
      }
    );
  }, [API_KEY]);

  if (loading) {
    return (
      <div className="layout">
        <Sidebar />
        <main className="weather-content">
          <h1>Loading Weather...</h1>
        </main>
      </div>
    );
  }

  if (!weather || weather.error) {
    return (
      <div className="layout">
        <Sidebar />
        <main className="weather-content">
          <h1>Weather API Error</h1>
          <pre>
            {JSON.stringify(
              weather,
              null,
              2
            )}
          </pre>
        </main>
      </div>
    );
  }

  const temp =
    weather.current.temp_c;

  const humidity =
    weather.current.humidity;

  const uv =
    weather.current.uv;

  const condition =
    weather.current.condition.text;

  const feelsLike =
    weather.current.feelslike_c;

  const wind =
    weather.current.wind_kph;

  const morningRoutine = [];
  const afternoonRoutine = [];
  const nightRoutine = [];

  if (uv >= 6) {
    morningRoutine.push(
      "Apply SPF 50+ sunscreen"
    );

    afternoonRoutine.push(
      "Re-apply sunscreen every 2 hours"
    );
  }

  if (temp >= 30) {
    morningRoutine.push(
      "Use a lightweight gel moisturizer"
    );

    afternoonRoutine.push(
      "Drink plenty of water"
    );

    afternoonRoutine.push(
      "Avoid excessive sun exposure"
    );
  }

  if (humidity >= 60) {
    nightRoutine.push(
      "Cleanse thoroughly to remove excess oil"
    );
  }

  if (humidity < 45) {
    nightRoutine.push(
      "Apply a richer moisturizer before sleep"
    );
  }

  if (
    condition.toLowerCase().includes("rain")
  ) {
    nightRoutine.push(
      "Double cleanse to remove pollutants"
    );
  }

  if (morningRoutine.length === 0) {
    morningRoutine.push(
      "Follow your regular skincare routine"
    );
  }

  if (afternoonRoutine.length === 0) {
    afternoonRoutine.push(
      "Stay hydrated and protect your skin"
    );
  }

  if (nightRoutine.length === 0) {
    nightRoutine.push(
      "Maintain your regular night-time routine"
    );
  }

  return (
    <div className="layout">
      <Sidebar />

      <main className="weather-content">

        <div className="weather-header">
          <h1>Weather-Based Care</h1>

          <p>
            Personalized skincare
            recommendations based on
            current weather conditions.
          </p>
        </div>

        <div className="weather-card">

          <div>
            <h2>
              📍 {weather.location.name},{" "}
              {weather.location.region}
            </h2>

            <p>{condition}</p>

            <p>
              Feels Like: {feelsLike}°C
            </p>

            <p>
              Wind: {wind} km/h
            </p>
          </div>

          <div className="weather-stats">

            <div>
              <span>{temp}°C</span>
              <p>Temperature</p>
            </div>

            <div>
              <span>{humidity}%</span>
              <p>Humidity</p>
            </div>

            <div>
              <span>{uv}</span>
              <p>UV Index</p>
            </div>

          </div>

        </div>

        <div className="weather-grid">

          <div className="info-card">

            <h3>
              Skin Risk Analysis
            </h3>

            <p>
              <strong>
                UV Exposure:
              </strong>{" "}
              {uv >= 6
                ? "High"
                : "Moderate"}
            </p>

            <p>
              <strong>
                Dehydration Risk:
              </strong>{" "}
              {humidity < 45
                ? "High"
                : "Moderate"}
            </p>

            <p>
              <strong>
                Oiliness Risk:
              </strong>{" "}
              {humidity > 60
                ? "High"
                : "Moderate"}
            </p>

          </div>

        </div>

        <div className="routine-card">

          <h2>
            Today's Personalized Care
          </h2>

          <div className="routine-grid">

            <div>
              <h3>🌅 Morning</h3>

              <ul>
                {morningRoutine.map(
                  (
                    item,
                    index
                  ) => (
                    <li key={index}>
                      {item}
                    </li>
                  )
                )}
              </ul>
            </div>

            <div>
              <h3>☀ Afternoon</h3>

              <ul>
                {afternoonRoutine.map(
                  (
                    item,
                    index
                  ) => (
                    <li key={index}>
                      {item}
                    </li>
                  )
                )}
              </ul>
            </div>

            <div>
              <h3>🌙 Night</h3>

              <ul>
                {nightRoutine.map(
                  (
                    item,
                    index
                  ) => (
                    <li key={index}>
                      {item}
                    </li>
                  )
                )}
              </ul>
            </div>

          </div>

        </div>

      </main>
    </div>
  );
}