"""EPA - Environmental Protection Agency API Module"""
import requests

BASE_URL = "https://data.epa.gov/efservice"
ECHO_BASE = "https://echo.epa.gov/api/rest_lookups"
HEADERS = {'Accept': 'application/json'}

def get_air_quality(count=20):
    """Fetch air quality data from EPA AirData."""
    try:
        url = "https://aqs.epa.gov/data/api/dailyData/byState?email=test@test.com&key=test&param=44201&bdate=20250101&edate=20250131&state=06"
        # Fallback to Envirofacts
        url = f"{BASE_URL}/WATER_SYSTEM/ROWS/0:{count}/JSON"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json() if isinstance(resp.json(), list) else []
            return [{
                'title': r.get('PWS_NAME', r.get('WATER_SYSTEM_NAME', 'Unknown System')),
                'description': f"State: {r.get('STATE_CODE', '')} | Population: {r.get('POPULATION_SERVED_COUNT', '')}",
                'date': r.get('LAST_REPORTED_DATE', ''),
                'link': 'https://echo.epa.gov/',
                'state': r.get('STATE_CODE', '')
            } for r in data[:count]]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_facility_info(count=20):
    """Fetch EPA regulated facility data."""
    try:
        url = f"{BASE_URL}/PCS_PERMIT_FACILITY/ROWS/0:{count}/JSON"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json() if isinstance(resp.json(), list) else []
            return [{
                'title': r.get('FACILITY_NAME', 'Unknown'),
                'description': f"Permit: {r.get('NPDES', '')} | City: {r.get('CITY', '')} | State: {r.get('STATE_CODE', '')}",
                'date': '',
                'link': f"https://echo.epa.gov/detailed-facility-report?fid={r.get('NPDES', '')}",
            } for r in data[:count]]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_toxic_releases(count=20):
    """Fetch Toxic Release Inventory data."""
    try:
        url = f"{BASE_URL}/TRI_FACILITY/ROWS/0:{count}/JSON"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json() if isinstance(resp.json(), list) else []
            return [{
                'title': r.get('FACILITY_NAME', 'Unknown'),
                'description': f"Industry: {r.get('PRIMARY_SIC', '')} | City: {r.get('CITY_NAME', '')}, {r.get('STATE_ABBR', '')}",
                'date': str(r.get('REPORTING_YEAR', '')),
                'link': f"https://enviro.epa.gov/triexplorer/",
            } for r in data[:count]]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_epa_data(api_key=None, params=None):
    sub = (params or {}).get('sub_section', 'water_systems')
    mapping = {
        'water_systems': get_air_quality,
        'facilities': get_facility_info,
        'toxic_releases': get_toxic_releases,
    }
    fn = mapping.get(sub, mapping['water_systems'])
    return {"results": fn(), "source": "EPA Envirofacts", "endpoint": sub}

def get_metadata():
    return {
        "name": "Environmental Protection Agency",
        "acronym": "EPA",
        "description": "Environmental data including water systems, facility permits, and toxic releases",
        "endpoints": ["Water Systems", "Regulated Facilities", "Toxic Release Inventory"],
        "sub_sections": [
            {"id": "water_systems", "name": "Water Systems"},
            {"id": "facilities", "name": "Regulated Facilities"},
            {"id": "toxic_releases", "name": "Toxic Release Inventory"},
        ],
        "has_search": False,
        "auth_required": False,
        "base_url": "https://data.epa.gov/efservice",
        "data_categories": ["Environmental", "Health", "Compliance", "Pollution"]
    }
