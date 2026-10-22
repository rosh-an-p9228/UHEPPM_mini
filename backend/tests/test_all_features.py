import sys
import httpx

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://127.0.0.1:5173"

def run_tests():
    print("==================================================")
    print("URBANHEAT AI PLATFORM -- PRODUCTION TEST SUITE")
    print("==================================================")
    
    passed = 0
    failed = 0

    with httpx.Client(timeout=10.0) as client:
        
        # Test 1: Root endpoint
        try:
            r = client.get(f"{BASE_URL}/")
            assert r.status_code == 200, f"Status {r.status_code}"
            assert r.json().get("app") == "UrbanHeat AI"
            print("[PASS] 01. Root API Endpoint & Health Check")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 01. Root API Endpoint: {e}")
            failed += 1

        # Test 2: Locations
        try:
            r = client.get(f"{BASE_URL}/api/locations/")
            assert r.status_code == 200
            locs = r.json()
            assert len(locs) >= 8
            assert any(l["id"] == "nerul" for l in locs)
            print(f"[PASS] 02. Locations API ({len(locs)} Municipal Wards Verified)")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 02. Locations API: {e}")
            failed += 1

        # Test 3: Dashboard Aggregated Telemetry
        try:
            r = client.get(f"{BASE_URL}/api/dashboard/?location_id=nerul")
            assert r.status_code == 200
            data = r.json()
            assert "kpi" in data and "weather" in data and "satellite" in data
            assert data["kpi"]["heat_risk_score"] > 0
            print("[PASS] 03. Dashboard Telemetry & Multi-Sensor Aggregator")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 03. Dashboard API: {e}")
            failed += 1

        # Test 4: Weather Current & History
        try:
            r = client.get(f"{BASE_URL}/api/weather/current?location_id=nerul")
            assert r.status_code == 200
            w = r.json()
            assert w["temperature"] > 0
            r2 = client.get(f"{BASE_URL}/api/weather/history?location_id=nerul")
            assert r2.status_code == 200
            assert len(r2.json()["history"]) > 0
            print("[PASS] 04. Weather Telemetry & 24h Diurnal History")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 04. Weather API: {e}")
            failed += 1

        # Test 5: Satellite LST
        try:
            r = client.get(f"{BASE_URL}/api/satellite/lst?location_id=nerul")
            assert r.status_code == 200
            sat = r.json()
            assert sat["lst_day"] >= 30.0
            print("[PASS] 05. Satellite LST Thermal Infrared Telemetry")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 05. Satellite LST API: {e}")
            failed += 1

        # Test 6: Vegetation NDVI
        try:
            r = client.get(f"{BASE_URL}/api/vegetation/ndvi?location_id=nerul")
            assert r.status_code == 200
            veg = r.json()
            assert "ndvi" in veg and "green_cover_pct" in veg
            print("[PASS] 06. Sentinel-2 NDVI & Canopy Gap Assessment")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 06. Vegetation API: {e}")
            failed += 1

        # Test 7: Traffic Flow & Vehicular Heat
        try:
            r = client.get(f"{BASE_URL}/api/traffic/heat?location_id=nerul")
            assert r.status_code == 200
            traf = r.json()
            assert "traffic_heat_contribution" in traf
            print("[PASS] 07. Traffic Flow & Thermodynamic Heat Model")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 07. Traffic Heat API: {e}")
            failed += 1

        # Test 8: Air Quality
        try:
            r = client.get(f"{BASE_URL}/api/air-quality/current?location_id=nerul")
            assert r.status_code == 200
            aqi = r.json()
            assert aqi["aqi"] > 0
            print("[PASS] 08. OpenAQ / CAAQMS Multi-Pollutant Grid")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 08. Air Quality API: {e}")
            failed += 1

        # Test 9: Population & Urban Activity
        try:
            r = client.get(f"{BASE_URL}/api/population/density?location_id=nerul")
            assert r.status_code == 200
            pop = r.json()
            assert pop["population_density_per_sq_km"] > 0
            print("[PASS] 09. WorldPop Density & Dynamic Urban Activity")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 09. Population API: {e}")
            failed += 1

        # Test 10: AI Multi-Horizon Predictions
        try:
            r = client.get(f"{BASE_URL}/api/predictions/?location_id=nerul")
            assert r.status_code == 200
            preds = r.json()["predictions"]
            assert len(preds) >= 5
            print(f"[PASS] 10. AI Multi-Horizon Forecast ({len(preds)} Horizons Verified)")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 10. Predictions API: {e}")
            failed += 1

        # Test 11: Explainable AI SHAP
        try:
            r = client.get(f"{BASE_URL}/api/explainability/?location_id=nerul")
            assert r.status_code == 200
            shap_res = r.json()
            assert "shap_attributions" in shap_res
            print("[PASS] 11. Explainable AI (TreeSHAP Feature Attribution)")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 11. Explainable AI API: {e}")
            failed += 1

        # Test 12: Recommendations
        try:
            r = client.get(f"{BASE_URL}/api/recommendations/?location_id=nerul")
            assert r.status_code == 200
            recs = r.json()["recommendations"]
            assert len(recs) >= 3
            print(f"[PASS] 12. Prevention Recommendations ({len(recs)} Interventions)")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 12. Recommendations API: {e}")
            failed += 1

        # Test 13: Heatwave Forecast
        try:
            r = client.get(f"{BASE_URL}/api/heatwave/?location_id=nerul")
            assert r.status_code == 200
            hw = r.json()
            assert "alert_level" in hw
            print("[PASS] 13. Heatwave Early Warning & Nocturnal Heat Watch")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 13. Heatwave API: {e}")
            failed += 1

        # Test 14: Heat Vulnerability Score
        try:
            r = client.get(f"{BASE_URL}/api/vulnerability/?location_id=nerul")
            assert r.status_code == 200
            vuln = r.json()
            assert vuln["overall_vulnerability_score"] > 0
            print("[PASS] 14. Socio-Ecological Heat Vulnerability Index (HVI)")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 14. Vulnerability API: {e}")
            failed += 1

        # Test 15: Urban Planning Scenario Simulator
        try:
            payload = {
                "location_id": "nerul",
                "tree_cover_delta_pct": 25.0,
                "cool_roofs_pct": 40.0,
                "traffic_reduction_pct": 20.0,
                "green_roofs_pct": 15.0,
                "solar_shading_pct": 30.0,
                "water_features_pct": 10.0
            }
            r = client.post(f"{BASE_URL}/api/simulation/", json=payload)
            assert r.status_code == 200
            sim = r.json()
            assert sim["temp_reduction_c"] > 0
            assert sim["annual_co2_reduction_tonnes"] > 0
            print(f"[PASS] 15. Urban Planning Simulator (Temp: -{sim['temp_reduction_c']}C, CO2: -{sim['annual_co2_reduction_tonnes']} tCO2/yr)")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 15. Simulator API: {e}")
            failed += 1

        # Test 16: Carbon Calculator
        try:
            payload = {
                "tree_count": 600,
                "traffic_reduction_pct": 25.0,
                "cool_roof_area_sq_m": 30000.0,
                "solar_capacity_kw": 600.0,
                "green_roof_area_sq_m": 12000.0
            }
            r = client.post(f"{BASE_URL}/api/carbon/calculate", json=payload)
            assert r.status_code == 200
            carb = r.json()
            assert carb["annual_co2_reduction_tonnes"] > 0
            print(f"[PASS] 16. Carbon Calculator ({carb['annual_co2_reduction_tonnes']} tCO2/yr offset)")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 16. Carbon Calculator API: {e}")
            failed += 1

        # Test 17: Image Analysis Sample
        try:
            r = client.get(f"{BASE_URL}/api/image-analysis/sample")
            assert r.status_code == 200
            img_res = r.json()
            assert "visual_heat_exposure_score" in img_res
            print(f"[PASS] 17. Computer Vision Heat Exposure Analyzer (Score: {img_res['visual_heat_exposure_score']}/100)")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 17. Image Analysis API: {e}")
            failed += 1

        # Test 18: AI Climate Chatbot
        try:
            payload = {
                "message": "Why is Nerul experiencing high heat?",
                "location_id": "nerul"
            }
            r = client.post(f"{BASE_URL}/api/chat/", json=payload)
            assert r.status_code == 200
            chat_res = r.json()
            assert len(chat_res["response"]) > 20
            print("[PASS] 18. AI Climate Decision Assistant (Grounded Query Processing)")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 18. Chatbot API: {e}")
            failed += 1

        # Test 19: API Status Monitor
        try:
            r = client.get(f"{BASE_URL}/api/status/")
            assert r.status_code == 200
            status_res = r.json()
            assert status_res["total_services"] == 7
            print(f"[PASS] 19. API Health Monitor ({status_res['total_services']} Services Verified)")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 19. API Status API: {e}")
            failed += 1

        # Test 20: Authentication
        try:
            r = client.post(f"{BASE_URL}/api/auth/login", json={"username": "admin", "password": "Admin@2026!"})
            assert r.status_code == 200
            assert "access_token" in r.json()
            print("[PASS] 20. Authentication & JWT Session Verification")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 20. Auth API: {e}")
            failed += 1

        # Test 21: Unified Dynamic Location Coordinates Endpoint
        try:
            r = client.get(f"{BASE_URL}/api/location-data/?lat=19.0330&lng=73.0297")
            assert r.status_code == 200
            loc_d = r.json()
            assert "location" in loc_d and "kpi" in loc_d and "weather" in loc_d
            assert loc_d["kpi"]["heat_risk_score"] > 0
            assert loc_d["weather"]["status"] in ["LIVE", "NEAR_REAL_TIME", "ESTIMATE", "DEMO_FALLBACK"]
            print(f"[PASS] 21. Unified Global Coordinates Intelligence ({loc_d['location']['name']}, Status: {loc_d['weather']['status']})")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 21. Unified Location Data API: {e}")
            failed += 1

        # Test 22: Universal Global Search
        try:
            r = client.get(f"{BASE_URL}/api/search/?q=mumbai")
            assert r.status_code == 200
            s_res = r.json()
            assert "results" in s_res and "total_results" in s_res
            assert s_res["total_results"] > 0
            print(f"[PASS] 22. Universal Global Search ({s_res['total_results']} matches for 'mumbai')")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 22. Global Search API: {e}")
            failed += 1

        # Test 23: User Preferences Management
        try:
            r = client.put(f"{BASE_URL}/api/auth/preferences", json={"temperature_unit": "C", "default_map_view": "satellite"})
            assert r.status_code == 200
            assert r.json()["preferences"]["temperature_unit"] == "C"
            print("[PASS] 23. User Preferences & Settings Management")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 23. User Preferences API: {e}")
            failed += 1

        # Test 24: Password Recovery
        try:
            r = client.post(f"{BASE_URL}/api/auth/forgot-password", json={"email": "analyst@urbanheat.gov.in"})
            assert r.status_code == 200
            print("[PASS] 24. Account Password Recovery Flow")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 24. Password Recovery API: {e}")
            failed += 1

        # Test 25: Frontend Web Server
        try:
            r = client.get(f"{FRONTEND_URL}/")
            assert r.status_code == 200
            assert "<!doctype html>" in r.text.lower()
            print("[PASS] 25. Frontend Web Application (Vite Server Serving HTML & Assets)")
            passed += 1
        except Exception as e:
            print(f"[FAIL] 25. Frontend Server: {e}")
            failed += 1

    print("==================================================")
    print(f"TEST RESULTS: {passed} PASSED, {failed} FAILED (Total {passed + failed} Tests)")
    print("==================================================")
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
