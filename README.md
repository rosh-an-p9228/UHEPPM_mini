# Urban Heat Entrapment Prediction and Prevention Model (UrbanHeat AI)

> **"Predict. Understand. Prevent Urban Heat."**

An AI-powered urban climate intelligence and decision support platform that monitors microclimate heat entrapment using multi-satellite Earth observation (MODIS LST, Landsat 9 TIRS, Copernicus Sentinel-2 MSI), live IoT sensor fusion (OpenWeather, OpenAQ/CPCB, TomTom Traffic Flow), machine learning (multi-horizon XGBoost thermal regressors), Explainable AI (TreeSHAP additive attribution), and physics-informed urban planning simulation.

---

## 🌟 Key Pillars & Features

1. **GIS Interactive Command Center**:
   - Leaflet.js map with multiple thematic layers (Google Earth Engine roadmap, Satellite LST thermal overlay, NDVI canopy vegetation, arterial traffic friction, population vulnerability, civic cooling shelters).
   - Dynamic slide-over ward dossier with real-time thermodynamic metrics.

2. **Multi-Source Sensor & Earth Observation Fusion**:
   - **OpenWeather / CAAQMS**: 2m atmospheric temperature, relative humidity, wind speed, barometric pressure, solar UV index.
   - **Satellite LST (MODIS / Landsat 9)**: Daytime surface skin radiance vs nocturnal thermal entrapment.
   - **Sentinel-2 MSI (Copernicus)**: $10\text{m}$ resolution NDVI vegetation index & municipal canopy deficit calculation.
   - **TomTom Traffic Flow API**: Arterial speed, congestion ratio, and thermodynamic combustion heat modeling.
   - **OpenAQ / CPCB**: Air quality index (AQI), PM2.5, PM10, $\text{NO}_2$, $\text{SO}_2$, $\text{O}_3$, and longwave radiation trapping.
   - **WorldPop & OpenStreetMap**: $100\text{m}$ population density disaggregation, sensitive infrastructure mapping (schools, hospitals), and dynamic urban activity modeling.

3. **Predictive Machine Learning Engine**:
   - Multi-horizon XGBoost thermal regressors with 95% confidence intervals (+1h, +3h, +6h, +24h, Tomorrow Peak).
   - Calibrated 0–100 **Heat Risk Index** and IPCC AR6 **Heat Vulnerability Index (HVI)**.

4. **Explainable AI (TreeSHAP)**:
   - Decomposes local risk scores into exact additive Shapley contributions for each thermodynamic factor.
   - Natural language physical explanations for municipal planners and citizens.

5. **Interactive Urban Planning Simulator**:
   - Dual-view microclimate scenario simulator with real-time responsive sliders:
     * Tree canopy expansion ($0$ to $+50\%$)
     * High-albedo cool roofs ($0$ to $100\%$)
     * Arterial traffic reduction ($0$ to $-50\%$)
     * Green roof infrastructure ($0$ to $+50\%$)
     * Pedestrian solar shading ($0$ to $+50\%$)
     * Urban wetlands & water misting ($0$ to $+30\%$)
   - Calculates projected cooling relief ($\Delta^\circ\text{C}$), risk score mitigation ($\Delta\%$), and annual carbon avoidance ($\text{tCO}_2/\text{year}$).

6. **Computer Vision Street & Drone Image Analyzer**:
   - Semantic segmentation of street photos into vegetative canopy, built-up concrete, asphalt roadway, and shadows.
   - Computes material-grounded **Visual Heat Exposure Scores** ($0\text{--}100$).

7. **Carbon Reduction & Sequestration Calculator**:
   - Models IPCC/EPA urban greenhouse gas emission avoidance and vegetative carbon sequestration.

8. **AI Climate Decision Support Assistant**:
   - Context-grounded municipal climate chatbot providing policy formulation, ward comparisons, and intervention advice.

9. **Multi-Lingual Localization (11 Indian & International Languages)**:
   - Full native translation catalogs: English, Hindi (हिन्दी), Marathi (मराठी), Gujarati (ગુજરાતી), Bengali (বাংলা), Tamil (தமிழ்), Telugu (తెలుగు), Kannada (ಕನ್ನಡ), Malayalam (മലയാളം), Punjabi (ਪੰਜਾਬੀ), Urdu (اردو).

10. **Scientific Data Transparency & Fallback Engine**:
    - Transparent `DataSourceBadge` indicators distinguishing between **Live API Observations**, **Periodic Satellite Overpasses**, and **Calibrated Demo Datasets**.

---

## 🏗️ System Architecture

### 1. High-Level System Architecture Diagram

```mermaid
graph TB
    subgraph "User Layer"
        User[End User / Municipal Planner / Citizen]
        Frontend[React Frontend<br/>Tailwind CSS + Leaflet GIS + i18n 11 Languages]
    end
    
    subgraph "API Layer"
        API[FastAPI REST API Server<br/>Uvicorn ASGI • Port 8000]
        Router[Modular Route Handlers<br/>18 API Routers]
    end
    
    subgraph "Service Layer"
        Geocoding[Geocoding Service]
        Weather[Weather Service]
        Satellite[Satellite Earth Engine Service]
        Vegetation[Vegetation & NDVI Service]
        Traffic[Traffic Dynamics Service]
        Pollution[Air Quality Service]
        Population[Demographics Service]
        HeatModel[XGBoost Thermal Regressor]
        SHAP[TreeSHAP Explainer Engine]
        Recommendation[Urban Intervention Engine]
        AIAssistant[AI Climate Policy Chatbot]
    end
    
    subgraph "Data Persistence Layer"
        SQLite[(SQLite Database<br/>urban_heat.db)]
        MunicipalGIS[(Municipal Ward Boundaries & Geometries)]
    end
    
    subgraph "External Telemetry & Satellite Ingestion"
        OpenWeather[OpenWeatherMap API]
        GoogleMaps[Google Geocoding & Maps]
        OpenStreet[OpenStreetMap Nominatim]
        TomTom[TomTom Traffic Flow API]
        OpenAQ[OpenAQ / CPCB Air Quality]
        MODIS[MODIS Aqua/Terra 1km LST]
        Landsat[Landsat 9 TIRS 30m LST]
        Sentinel[Copernicus Sentinel-2 MSI 10m NDVI]
    end
    
    User -->|HTTP Request| Frontend
    Frontend -->|REST API Calls| API
    API --> Router
    
    Router --> Geocoding
    Router --> Weather
    Router --> Satellite
    Router --> Vegetation
    Router --> Traffic
    Router --> Pollution
    Router --> Population
    Router --> HeatModel
    Router --> SHAP
    Router --> Recommendation
    Router --> AIAssistant
    
    Geocoding --> MunicipalGIS
    Geocoding --> GoogleMaps
    Geocoding --> OpenStreet
    Weather --> OpenWeather
    Satellite --> MODIS
    Satellite --> Landsat
    Satellite --> Sentinel
    Vegetation --> Sentinel
    Traffic --> TomTom
    Pollution --> OpenAQ
    
    HeatModel --> SQLite
    SHAP --> HeatModel
    Recommendation --> HeatModel
    Recommendation --> SHAP
    Router --> SQLite
    
    API -->|JSON Telemetry Response| Frontend
    Frontend -->|Interactive Visual Dashboard| User
```

---

### 2. End-to-End Data Flow Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Urban Planner
    participant FE as React Frontend (Port 5173)
    participant API as FastAPI Backend (Port 8000)
    participant GEO as Geocoding Service
    participant SENS as Parallel Ingestion Engine
    participant ML as XGBoost & TreeSHAP ML
    participant DB as SQLite (urban_heat.db)

    User->>FE: Select Location on Map or Search Ward (lat, lng)
    FE->>API: GET /api/location-data/?lat=X&lng=Y
    
    API->>GEO: Resolve Coordinates & Boundaries
    alt Known Municipal Ward
        GEO-->>API: Municipal Ward Dossier & Pre-computed Baseline
    else Custom Coordinate
        GEO->>GEO: Reverse Geocode via Google / OpenStreetMap
        GEO-->>API: Formatted Address & Geographic Bounds
    end

    par Parallel Environmental Sensor Ingestion
        API->>SENS: Fetch Weather (Temp, Humidity, Wind, UV)
        SENS-->>API: OpenWeather Telemetry
    and
        API->>SENS: Fetch Satellite LST (MODIS / Landsat 9)
        SENS-->>API: Daytime LST & Nocturnal Surface Radiance
    and
        API->>SENS: Fetch Sentinel-2 Vegetation Index
        SENS-->>API: 10m Band 8/Band 4 NDVI & Canopy Coverage %
    and
        API->>SENS: Fetch Arterial Traffic Friction
        SENS-->>API: TomTom Flow Speed & Vehicular Heat Contribution
    and
        API->>SENS: Fetch Atmospheric Pollution
        SENS-->>API: OpenAQ AQI, PM2.5, PM10 & Radiation Trap Ratio
    end

    API->>ML: Run Predictive Thermal Pipeline (Weather + LST + NDVI + Traffic + AQI)
    ML->>ML: XGBoost Multi-Horizon Forecast (+1h, +3h, +6h, +24h)
    ML->>ML: TreeSHAP Exact Additive Factor Attribution
    ML-->>API: Heat Risk Index (0-100), Thermal Forecasts & SHAP Attributions

    API->>DB: Log Ingestion Record & Update Ward Historical Series
    DB-->>API: Transaction Success

    API-->>FE: Consolidated JSON Telemetry Payload
    FE->>User: Render Live Map Overlays, Charts, Gauges & Actionable Advisories
```

---

### 3. Component & Service Architecture Mapping

```mermaid
graph LR
    subgraph "Frontend Views (React)"
        Landing[Landing Hero & Overview]
        HeatMap[GIS Heat Map & Earth Engine]
        GreenCover[Green Canopy & NDVI Index]
        TrafficTab[Arterial Traffic & Heat]
        Prediction[Multi-Horizon AI Forecast]
        Simulation[Physics Planning Simulator]
        ExplainableAI[TreeSHAP Risk Decomposition]
        AIAssistantUI[AI Climate Policy Assistant]
        ImageCV[Street CV Segmenter]
    end

    subgraph "API REST Endpoints"
        EP_Dashboard[/api/dashboard/]
        EP_LocData[/api/location-data/]
        EP_Satellite[/api/satellite/lst/]
        EP_Veg[/api/vegetation/ndvi/]
        EP_Traffic[/api/traffic/current/]
        EP_Predict[/api/predictions/]
        EP_Sim[/api/simulation/]
        EP_Explain[/api/explainability/]
        EP_Chat[/api/chat/]
        EP_CV[/api/image-analysis/segment/]
    end

    subgraph "Backend Services & ML"
        Svc_Location[Geocoding & Municipal Wards]
        Svc_Weather[Weather Ingestion Service]
        Svc_Sat[Satellite Earth Engine Service]
        Svc_Veg[Vegetation & Canopy Service]
        Svc_Traf[Traffic Modeling Service]
        ML_Model[XGBoost Heat Model]
        ML_Sim[Physics Microclimate Simulator]
        ML_SHAP[TreeSHAP Attribution Engine]
        Svc_AI[LLM Climate Policy Agent]
        ML_CV[Color-Band Semantic Segmenter]
    end

    Landing --> EP_Dashboard
    HeatMap --> EP_LocData
    GreenCover --> EP_Veg
    TrafficTab --> EP_Traffic
    Prediction --> EP_Predict
    Simulation --> EP_Sim
    ExplainableAI --> EP_Explain
    AIAssistantUI --> EP_Chat
    ImageCV --> EP_CV

    EP_Dashboard --> Svc_Location
    EP_LocData --> Svc_Weather
    EP_LocData --> Svc_Sat
    EP_Satellite --> Svc_Sat
    EP_Veg --> Svc_Veg
    EP_Traffic --> Svc_Traf
    EP_Predict --> ML_Model
    EP_Sim --> ML_Sim
    EP_Explain --> ML_SHAP
    EP_Chat --> Svc_AI
    EP_CV --> ML_CV
```

---

### 4. Entity-Relationship (ER) Database Architecture

```mermaid
erDiagram
    LOCATIONS ||--o{ WEATHER_DATA : "records"
    LOCATIONS ||--o{ SATELLITE_DATA : "measures"
    LOCATIONS ||--o{ VEGETATION_DATA : "monitors"
    LOCATIONS ||--o{ TRAFFIC_DATA : "tracks"
    LOCATIONS ||--o{ AIR_QUALITY_DATA : "samples"
    LOCATIONS ||--o{ POPULATION_DATA : "houses"
    LOCATIONS ||--o{ PREDICTIONS : "generates"

    LOCATIONS {
        string id PK "Unique location slug (e.g., nerul)"
        string name "Ward / Sector name"
        string city "City name"
        string state "State name"
        string country "Country ISO"
        float latitude "Geographic latitude"
        float longitude "Geographic longitude"
        float area_sq_km "Ward area"
        integer baseline_population "Demographic baseline"
        float baseline_ndvi "Baseline vegetation index"
        float baseline_lst "Baseline surface temperature"
        float baseline_temp "Baseline air temperature"
        integer baseline_aqi "Baseline air quality index"
        float baseline_traffic_congestion "Baseline congestion ratio"
        json boundary_geojson "Ward polygon boundary"
    }

    WEATHER_DATA {
        integer id PK "Primary key"
        string location_id FK "References LOCATIONS(id)"
        float temperature "2m atmospheric temp (°C)"
        float humidity "Relative humidity (%)"
        float wind_speed "Wind velocity (km/h)"
        float pressure "Atmospheric pressure (hPa)"
        float uv_index "Solar ultraviolet index"
        string condition "Weather condition"
        float feels_like "Apparent thermal sensation (°C)"
        datetime timestamp "Observation timestamp"
        string source "Data origin (live/cached/demo)"
        string status "Pipeline ingestion status"
    }

    SATELLITE_DATA {
        integer id PK "Primary key"
        string location_id FK "References LOCATIONS(id)"
        float lst_day "Daytime Land Surface Temp (°C)"
        float lst_night "Nocturnal Land Surface Temp (°C)"
        string thermal_intensity "Entrapment severity classification"
        datetime timestamp "Satellite overpass timestamp"
        string source "Satellite instrument (MODIS/Landsat/Sentinel)"
        string status "Data quality status"
    }

    VEGETATION_DATA {
        integer id PK "Primary key"
        string location_id FK "References LOCATIONS(id)"
        float ndvi "Normalized Difference Vegetation Index"
        float green_cover_pct "Canopy coverage percentage"
        float gap_pct "Deficit below municipal target"
        datetime timestamp "Observation timestamp"
        string source "Copernicus Sentinel-2 MSI"
        string status "Data quality status"
    }

    TRAFFIC_DATA {
        integer id PK "Primary key"
        string location_id FK "References LOCATIONS(id)"
        float congestion_index "Speed reduction ratio"
        float congestion_pct "Congestion percentage"
        float traffic_heat_contribution "Modeled anthropogenic heat (°C)"
        datetime timestamp "Telemetry timestamp"
        string source "TomTom Traffic Flow API"
        string status "Data quality status"
    }

    AIR_QUALITY_DATA {
        integer id PK "Primary key"
        string location_id FK "References LOCATIONS(id)"
        integer aqi "Air Quality Index"
        float pm25 "PM2.5 concentration (µg/m³)"
        float pm10 "PM10 concentration (µg/m³)"
        string category "Air quality band"
        datetime timestamp "Measurement timestamp"
        string source "OpenAQ / CPCB CAAQMS"
        string status "Data quality status"
    }

    POPULATION_DATA {
        integer id PK "Primary key"
        string location_id FK "References LOCATIONS(id)"
        float population_density_per_sq_km "People per km²"
        integer baseline_population "Total population"
        float area_sq_km "Ward area"
        datetime timestamp "Census/WorldPop timestamp"
    }

    PREDICTIONS {
        integer id PK "Primary key"
        string location_id FK "References LOCATIONS(id)"
        float predicted_temp_1h "+1 Hour forecast (°C)"
        float predicted_temp_3h "+3 Hour forecast (°C)"
        float predicted_temp_6h "+6 Hour forecast (°C)"
        float predicted_temp_24h "+24 Hour forecast (°C)"
        float confidence_lower "95% CI lower bound"
        float confidence_upper "95% CI upper bound"
        float heat_risk_score "Calibrated Risk Index (0-100)"
        string heat_risk_category "MODERATE / HIGH / EXTREME"
        datetime created_at "Inference timestamp"
    }
```

---

### 5. Technology Stack Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        React[React 19]
        Vite[Vite 8 Build & Dev Server]
        Tailwind[Tailwind CSS Modern Styling]
        Leaflet[Leaflet.js & React-Leaflet GIS]
        Lucide[Lucide React Icons]
        i18n[i18next 11-Language Engine]
        Axios[Axios HTTP Client]
    end

    subgraph "Backend Layer"
        Python[Python 3.10+]
        FastAPI[FastAPI 0.104+ REST Framework]
        Uvicorn[Uvicorn High-Performance ASGI]
        Pydantic[Pydantic v2 Schema Validation]
    end

    subgraph "Geospatial, ML & Scientific Intelligence"
        SQLite[SQLite Embedded Engine • urban_heat.db]
        XGBoost[XGBoost Thermal Regressors]
        TreeSHAP[TreeSHAP Factor Attribution]
        NumPy[NumPy Scientific Computing]
        PIL[Pillow Semantic Computer Vision]
        Httpx[Httpx Async Sensor Client]
    end

    subgraph "Satellite Earth Observation & Telemetry"
        OpenWeatherAPI[OpenWeather Atmospheric API]
        TomTomAPI[TomTom Traffic Flow API]
        OpenAQAPI[OpenAQ / CPCB Air Quality]
        MODIS_Sat[MODIS Terra/Aqua Thermal Radiance]
        Landsat_Sat[Landsat 9 TIRS 30m Microthermal]
        Sentinel_Sat[Copernicus Sentinel-2 MSI 10m NDVI]
    end

    React --> Vite
    React --> Tailwind
    React --> Leaflet
    React --> i18n
    React --> Axios
    
    Axios -->|JSON over HTTP| FastAPI
    FastAPI --> Uvicorn
    FastAPI --> Pydantic
    
    FastAPI --> SQLite
    FastAPI --> XGBoost
    FastAPI --> TreeSHAP
    FastAPI --> NumPy
    FastAPI --> PIL
    FastAPI --> Httpx
    
    Httpx --> OpenWeatherAPI
    Httpx --> TomTomAPI
    Httpx --> OpenAQAPI
    Httpx --> MODIS_Sat
    Httpx --> Landsat_Sat
    Httpx --> Sentinel_Sat
```

---

### 6. Clean Workspace Structure

```
UHE_mini/
├── backend/
│   ├── .env                 # API keys & configuration
│   ├── .env.example         # Environment template
│   ├── app/
│   │   ├── api/             # 18 Modular REST Route Handlers
│   │   │   ├── api_status.py
│   │   │   ├── auth.py
│   │   │   ├── carbon.py
│   │   │   ├── chatbot.py
│   │   │   ├── dashboard.py
│   │   │   ├── explainability.py
│   │   │   ├── heatwave.py
│   │   │   ├── image_analysis.py
│   │   │   ├── location_data.py
│   │   │   ├── locations.py
│   │   │   ├── pollution.py
│   │   │   ├── population.py
│   │   │   ├── predictions.py
│   │   │   ├── recommendations.py
│   │   │   ├── satellite.py
│   │   │   ├── search.py
│   │   │   ├── simulation.py
│   │   │   ├── traffic.py
│   │   │   ├── vegetation.py
│   │   │   ├── vulnerability.py
│   │   │   └── weather.py
│   │   ├── config.py        # Settings & transparent fallback engine
│   │   ├── database.py      # SQLite geospatial persistence (15 entities)
│   │   ├── main.py          # FastAPI application entrypoint
│   │   ├── ml/              # Machine learning, SHAP, CV segmenter & simulator
│   │   │   ├── carbon_calculator.py
│   │   │   ├── explain_shap.py
│   │   │   ├── feature_engineering.py
│   │   │   ├── heat_model.py
│   │   │   ├── hotspot_clustering.py
│   │   │   ├── image_segmenter.py
│   │   │   └── simulator_engine.py
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   │   └── schemas.py
│   │   ├── seed_data/       # Pre-seeded municipal ward datasets
│   │   │   └── seed_cities.py
│   │   └── services/        # External sensor & satellite ingestion services
│   │       ├── ai_assistant_service.py
│   │       ├── earth_engine_service.py
│   │       ├── geocoding_service.py
│   │       ├── pollution_service.py
│   │       ├── population_service.py
│   │       ├── satellite_service.py
│   │       ├── traffic_service.py
│   │       ├── vegetation_service.py
│   │       └── weather_service.py
│   └── tests/
│       └── test_all_features.py  # Comprehensive 21-test verification suite
├── frontend/
│   ├── dist/                # Production web application bundle
│   │   ├── assets/          # JavaScript, CSS & SVG graphics
│   │   └── index.html       # Production entry HTML
│   ├── public/              # Static assets served by Vite
│   │   └── assets/
│   ├── src/                 # React source code & translation catalogs
│   │   ├── assets/
│   │   ├── locales/         # 11 Indian & International language catalogs
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── i18n.js
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html           # Frontend entry HTML
│   ├── package.json         # Frontend dependencies & npm scripts
│   ├── package-lock.json
│   └── vite.config.js       # Vite configuration & /api reverse proxy
├── package.json             # Root workspace scripts
├── run_website.bat          # Windows one-click launcher
├── run_website.py           # Unified backend + frontend service manager
├── urban_heat.db            # SQLite database with pre-seeded municipal telemetry
└── README.md                # Comprehensive documentation & architecture
```

---

## 🚀 Quick Start (Running the Website)

**Prerequisites**: Python 3.10+, Node.js 18+

### Option A: One-Command Instant Launch (Recommended)
Start both backend & frontend together with **a single command**:

```bash
python run_website.py
```
*(On Windows, you can also simply double-click `run_website.bat` or run `npm start` / `npm run dev` from the root folder)*

This script will:
1. Verify and automatically self-heal all frontend bundles and static assets.
2. Launch the FastAPI backend server on port `8000`.
3. Launch the Vite frontend dev server on port `5173`.
4. Automatically open `http://localhost:5173/` in your default browser.

---

### Option B: Two-Terminal Launch

```bash
# Terminal 1: Backend
pip install fastapi uvicorn pydantic python-multipart pillow numpy httpx
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

---

### 🌐 Access Points & Verification
- **Application Dashboard (UI)**: [http://localhost:5173/](http://localhost:5173/)
- **FastAPI Documentation (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Live Telemetry Stream**: [http://127.0.0.1:8000/api/dashboard/?location_id=nerul](http://127.0.0.1:8000/api/dashboard/?location_id=nerul)
- **Run Diagnostic Tests**: `python -m backend.tests.test_all_features`

---

## 🛡️ Scientific Formulations

- **Normalized Difference Vegetation Index (NDVI)**:
  $$\text{NDVI} = \frac{\text{NIR}_{842\text{nm}} - \text{Red}_{665\text{nm}}}{\text{NIR}_{842\text{nm}} + \text{Red}_{665\text{nm}}}$$

- **Congestion Ratio**:
  $$\text{Congestion} = 1.0 - \frac{\text{Speed}_{\text{observed}}}{\text{Speed}_{\text{free-flow}}}$$

- **Estimated Vehicular Heat Contribution**:
  $$Q_{\text{traffic}} = (\text{Congestion} \times 16.0) + \max\left(0, \frac{50 - v}{50} \times 8.0\right) + \max(0, (T_{\text{amb}} - 30) \times 0.4)$$

- **Heat Vulnerability Index (HVI)**:
  $$\text{HVI} = (\text{Exposure} \times 0.45) + (\text{Sensitivity} \times 0.35) - (\text{AdaptiveCapacity} \times 0.20)$$

---

## 📜 Academic Attribution & License
Developed as a Major College Capstone Project in Urban Climate Intelligence, Geospatial Artificial Intelligence, and Sustainable City Planning.
