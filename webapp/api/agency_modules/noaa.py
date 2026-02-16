"""NOAA - National Oceanic and Atmospheric Administration API Module"""
import requests

NWS_BASE = "https://api.weather.gov"
HEADERS = {'User-Agent': 'OpenGovDash Research Tool 1.0', 'Accept': 'application/geo+json'}

def get_active_alerts(count=20):
    try:
        resp = requests.get(f"{NWS_BASE}/alerts/active", headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            features = resp.json().get('features', [])[:count]
            return [{
                'title': f.get('properties', {}).get('headline', ''),
                'description': (f.get('properties', {}).get('description', '') or '')[:300],
                'date': f.get('properties', {}).get('onset', ''),
                'link': f.get('properties', {}).get('uri', '') or f"https://alerts.weather.gov",
                'severity': f.get('properties', {}).get('severity', ''),
                'event': f.get('properties', {}).get('event', ''),
                'area': f.get('properties', {}).get('areaDesc', '')
            } for f in features]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_weather_forecast(lat=38.8894, lon=-77.0352):
    """Get forecast for a location (default: Washington DC)."""
    try:
        resp = requests.get(f"{NWS_BASE}/points/{lat},{lon}", headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            forecast_url = resp.json().get('properties', {}).get('forecast', '')
            if forecast_url:
                resp2 = requests.get(forecast_url, headers=HEADERS, timeout=15)
                if resp2.status_code == 200:
                    periods = resp2.json().get('properties', {}).get('periods', [])
                    return [{
                        'title': p.get('name', ''),
                        'description': p.get('detailedForecast', ''),
                        'date': p.get('startTime', ''),
                        'link': 'https://weather.gov',
                        'temperature': f"{p.get('temperature', '')}°{p.get('temperatureUnit', '')}",
                        'wind': f"{p.get('windSpeed', '')} {p.get('windDirection', '')}"
                    } for p in periods]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_noaa_data(api_key=None, params=None):
    sub = (params or {}).get('sub_section', 'alerts')
    mapping = {
        'alerts': get_active_alerts,
        'forecast': get_weather_forecast,
    }
    fn = mapping.get(sub, mapping['alerts'])
    return {"results": fn(), "source": "NOAA/NWS", "endpoint": sub}

def get_metadata():
    return {
        "name": "National Oceanic and Atmospheric Administration",
        "acronym": "NOAA",
        "description": "Weather alerts, forecasts, and climate data from the National Weather Service",
        "endpoints": ["Active Weather Alerts", "Weather Forecast"],
        "sub_sections": [
            {"id": "alerts", "name": "Active Weather Alerts"},
            {"id": "forecast", "name": "Weather Forecast (DC)"},
        ],
        "has_search": False,
        "auth_required": False,
        "base_url": "https://api.weather.gov",
        "data_categories": ["Weather", "Climate", "Environmental"]
    }
