import json
from datetime import datetime
from typing import Any, Dict, List, Optional
import sqlite3
import os
from .config import settings

# Lightweight high-performance database manager supporting GeoJSON, JSON storage, and spatial records
DB_PATH = "urban_heat.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

get_db = get_db_connection

def init_db():
    """Initialize database tables with complete schema"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Locations / Wards Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        country TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        boundary_geojson TEXT,
        area_sq_km REAL DEFAULT 5.0,
        baseline_population INTEGER DEFAULT 50000,
        baseline_ndvi REAL DEFAULT 0.25,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Weather Readings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id TEXT NOT NULL,
        temperature REAL NOT NULL,
        feels_like REAL NOT NULL,
        humidity REAL NOT NULL,
        wind_speed REAL NOT NULL,
        wind_deg REAL DEFAULT 0,
        uv_index REAL DEFAULT 5.0,
        pressure REAL DEFAULT 1012.0,
        rainfall REAL DEFAULT 0.0,
        cloud_cover REAL DEFAULT 10.0,
        condition TEXT DEFAULT 'Clear',
        source TEXT DEFAULT 'OpenWeather',
        is_demo BOOLEAN DEFAULT 0,
        recorded_at TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (location_id) REFERENCES locations (id)
    )
    """)
    
    # Satellite LST Observations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS satellite_observations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id TEXT NOT NULL,
        lst_day REAL NOT NULL,
        lst_night REAL NOT NULL,
        heat_intensity TEXT DEFAULT 'High',
        cloud_coverage REAL DEFAULT 5.0,
        sensor TEXT DEFAULT 'MODIS Terra/Aqua & Landsat 9',
        is_demo BOOLEAN DEFAULT 0,
        observation_date TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (location_id) REFERENCES locations (id)
    )
    """)
    
    # Vegetation / NDVI Readings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vegetation_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id TEXT NOT NULL,
        ndvi REAL NOT NULL,
        green_cover_pct REAL NOT NULL,
        tree_density_pct REAL NOT NULL,
        vegetation_class TEXT NOT NULL,
        sensor TEXT DEFAULT 'Sentinel-2 MSI',
        is_demo BOOLEAN DEFAULT 0,
        observation_date TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (location_id) REFERENCES locations (id)
    )
    """)
    
    # Traffic Heat Readings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS traffic_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id TEXT NOT NULL,
        congestion_index REAL NOT NULL,
        current_speed_kmh REAL NOT NULL,
        free_flow_speed_kmh REAL NOT NULL,
        delay_seconds REAL DEFAULT 0,
        estimated_vehicle_activity TEXT DEFAULT 'High',
        traffic_heat_contribution REAL NOT NULL,
        source TEXT DEFAULT 'TomTom Traffic API',
        is_demo BOOLEAN DEFAULT 0,
        recorded_at TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (location_id) REFERENCES locations (id)
    )
    """)
    
    # Air Quality Readings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS air_quality_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id TEXT NOT NULL,
        aqi INTEGER NOT NULL,
        category TEXT NOT NULL,
        pm25 REAL NOT NULL,
        pm10 REAL NOT NULL,
        no2 REAL NOT NULL,
        so2 REAL DEFAULT 12.0,
        o3 REAL DEFAULT 45.0,
        co REAL DEFAULT 0.8,
        source TEXT DEFAULT 'OpenAQ / CPCB',
        is_demo BOOLEAN DEFAULT 0,
        recorded_at TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (location_id) REFERENCES locations (id)
    )
    """)
    
    # Heat Predictions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS heat_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id TEXT NOT NULL,
        horizon TEXT NOT NULL, -- 1h, 3h, 6h, 24h, tomorrow
        predicted_temp REAL NOT NULL,
        confidence_lower REAL NOT NULL,
        confidence_upper REAL NOT NULL,
        heat_risk_score REAL NOT NULL,
        risk_category TEXT NOT NULL, -- SAFE, MODERATE, HIGH, EXTREME
        model_version TEXT DEFAULT 'XGBoost-v2.1',
        shap_factors_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (location_id) REFERENCES locations (id)
    )
    """)
    
    # Heatwave Alerts Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS heat_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id TEXT NOT NULL,
        alert_type TEXT NOT NULL,
        severity TEXT NOT NULL, -- Information, Warning, High, Critical
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        max_predicted_temp REAL,
        expected_duration_days INTEGER DEFAULT 1,
        recommended_actions_json TEXT,
        is_active BOOLEAN DEFAULT 1,
        valid_from TIMESTAMP NOT NULL,
        valid_until TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (location_id) REFERENCES locations (id)
    )
    """)
    
    # Prevention Recommendations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recommendations (
        id TEXT PRIMARY KEY,
        location_id TEXT NOT NULL,
        category TEXT NOT NULL, -- Vegetation, Buildings, Traffic, Pollution, Public Health
        title TEXT NOT NULL,
        reason TEXT NOT NULL,
        priority TEXT NOT NULL, -- LOW, MEDIUM, HIGH, CRITICAL
        expected_temp_reduction_min REAL NOT NULL,
        expected_temp_reduction_max REAL NOT NULL,
        expected_risk_reduction REAL NOT NULL,
        implementation_difficulty TEXT NOT NULL, -- Easy, Moderate, Complex
        cost_category TEXT NOT NULL, -- Low, Medium, High
        status TEXT DEFAULT 'Recommended',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (location_id) REFERENCES locations (id)
    )
    """)
    
    # Vulnerability Assessments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vulnerability_assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id TEXT NOT NULL,
        exposure_score REAL NOT NULL,
        sensitivity_score REAL NOT NULL,
        adaptive_capacity_score REAL NOT NULL,
        overall_vulnerability_score REAL NOT NULL,
        vulnerability_category TEXT NOT NULL, -- Low, Moderate, High, Extreme
        details_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (location_id) REFERENCES locations (id)
    )
    """)
    
    # Saved Simulation Scenarios Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS simulation_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id TEXT NOT NULL,
        scenario_name TEXT NOT NULL,
        tree_cover_delta_pct REAL DEFAULT 0,
        cool_roofs_pct REAL DEFAULT 0,
        traffic_reduction_pct REAL DEFAULT 0,
        green_roofs_pct REAL DEFAULT 0,
        solar_shading_pct REAL DEFAULT 0,
        water_features_pct REAL DEFAULT 0,
        initial_heat_risk REAL NOT NULL,
        simulated_heat_risk REAL NOT NULL,
        initial_temp REAL NOT NULL,
        simulated_temp REAL NOT NULL,
        annual_co2_reduction_tonnes REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (location_id) REFERENCES locations (id)
    )
    """)
    
    # Image Analysis History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS image_analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        tree_coverage_pct REAL NOT NULL,
        built_up_pct REAL NOT NULL,
        road_pct REAL NOT NULL,
        shade_pct REAL NOT NULL,
        vehicle_count INTEGER DEFAULT 0,
        visual_heat_exposure_score REAL NOT NULL,
        exposure_rating TEXT NOT NULL,
        detected_features_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # API Health & Status Log Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS api_status_logs (
        service_name TEXT PRIMARY KEY,
        status TEXT NOT NULL, -- Operational, Delayed, Unavailable, Demo Mode
        response_time_ms INTEGER DEFAULT 45,
        last_successful_update TIMESTAMP,
        last_error TEXT,
        endpoint_url TEXT,
        data_transparency_note TEXT
    )
    """)
    
    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        role TEXT DEFAULT 'analyst', -- admin, analyst, public
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
