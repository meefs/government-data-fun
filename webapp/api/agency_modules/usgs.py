"""USGS - United States Geological Survey API Module"""
import requests

HEADERS = {'Accept': 'application/json'}

def get_earthquakes(count=20, min_magnitude=2.5):
    """Fetch recent earthquake data."""
    try:
        url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&limit={count}&minmagnitude={min_magnitude}&orderby=time"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            features = resp.json().get('features', [])
            return [{
                'title': f.get('properties', {}).get('title', ''),
                'description': f"Magnitude: {f.get('properties', {}).get('mag', '')} | Type: {f.get('properties', {}).get('type', '')} | Depth: {f.get('geometry', {}).get('coordinates', [0,0,0])[2]}km",
                'date': f.get('properties', {}).get('time', ''),
                'link': f.get('properties', {}).get('url', ''),
                'magnitude': f.get('properties', {}).get('mag', ''),
                'place': f.get('properties', {}).get('place', ''),
                'tsunami': f.get('properties', {}).get('tsunami', 0)
            } for f in features]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_water_data(count=20):
    """Fetch real-time water data from USGS."""
    try:
        url = f"https://waterservices.usgs.gov/nwis/iv/?format=json&stateCd=CA&parameterCd=00060&siteStatus=active"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            ts = resp.json().get('value', {}).get('timeSeries', [])[:count]
            return [{
                'title': t.get('sourceInfo', {}).get('siteName', ''),
                'description': f"Variable: {t.get('variable', {}).get('variableDescription', '')} | Value: {t.get('values', [{}])[0].get('value', [{}])[0].get('value', '') if t.get('values') else 'N/A'}",
                'date': t.get('values', [{}])[0].get('value', [{}])[0].get('dateTime', '') if t.get('values') else '',
                'link': f"https://waterdata.usgs.gov/nwis/uv?site_no={t.get('sourceInfo', {}).get('siteCode', [{}])[0].get('value', '')}",
            } for t in ts]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_usgs_data(api_key=None, params=None):
    sub = (params or {}).get('sub_section', 'earthquakes')
    mapping = {
        'earthquakes': get_earthquakes,
        'water': get_water_data,
    }
    fn = mapping.get(sub, mapping['earthquakes'])
    return {"results": fn(), "source": "USGS", "endpoint": sub}

def get_metadata():
    return {
        "name": "United States Geological Survey",
        "acronym": "USGS",
        "description": "Earthquake data, water monitoring, and geological information",
        "endpoints": ["Recent Earthquakes", "Water Data"],
        "sub_sections": [
            {"id": "earthquakes", "name": "Recent Earthquakes"},
            {"id": "water", "name": "Water Monitoring (CA)"},
        ],
        "has_search": False,
        "auth_required": False,
        "base_url": "https://earthquake.usgs.gov",
        "data_categories": ["Geological", "Environmental", "Natural Hazards"]
    }
