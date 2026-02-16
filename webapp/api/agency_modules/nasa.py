"""NASA API Module"""
import requests

BASE_URL = "https://api.nasa.gov"
DEMO_KEY = "DEMO_KEY"
HEADERS = {'Accept': 'application/json'}

def get_apod(api_key=None, count=10):
    key = api_key or DEMO_KEY
    try:
        resp = requests.get(f"{BASE_URL}/planetary/apod?api_key={key}&count={count}", headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, dict):
                data = [data]
            return [{
                'title': r.get('title', ''),
                'description': (r.get('explanation', '') or '')[:300],
                'date': r.get('date', ''),
                'link': r.get('hdurl', r.get('url', '')),
                'media_type': r.get('media_type', '')
            } for r in data]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_neo(api_key=None):
    """Near Earth Objects."""
    key = api_key or DEMO_KEY
    try:
        resp = requests.get(f"{BASE_URL}/neo/rest/v1/neo/browse?api_key={key}", headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            neos = resp.json().get('near_earth_objects', [])[:20]
            return [{
                'title': n.get('name', ''),
                'description': f"Magnitude: {n.get('absolute_magnitude_h', '')} | Hazardous: {n.get('is_potentially_hazardous_asteroid', False)}",
                'date': n.get('orbital_data', {}).get('first_observation_date', ''),
                'link': n.get('nasa_jpl_url', ''),
                'hazardous': n.get('is_potentially_hazardous_asteroid', False)
            } for n in neos]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_mars_photos(api_key=None):
    key = api_key or DEMO_KEY
    try:
        resp = requests.get(f"{BASE_URL}/mars-photos/api/v1/rovers/curiosity/latest_photos?api_key={key}", headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            photos = resp.json().get('latest_photos', [])[:20]
            return [{
                'title': f"Sol {p.get('sol', '')} - {p.get('camera', {}).get('full_name', '')}",
                'description': f"Rover: {p.get('rover', {}).get('name', '')} | Camera: {p.get('camera', {}).get('name', '')}",
                'date': p.get('earth_date', ''),
                'link': p.get('img_src', ''),
            } for p in photos]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_nasa_data(api_key=None, params=None):
    sub = (params or {}).get('sub_section', 'apod')
    mapping = {
        'apod': lambda: get_apod(api_key),
        'neo': lambda: get_neo(api_key),
        'mars': lambda: get_mars_photos(api_key),
    }
    fn = mapping.get(sub, mapping['apod'])
    return {"results": fn(), "source": "NASA", "endpoint": sub}

def get_metadata():
    return {
        "name": "National Aeronautics and Space Administration",
        "acronym": "NASA",
        "description": "Astronomy pictures, near-earth objects, Mars rover photos",
        "endpoints": ["Astronomy Picture of the Day", "Near Earth Objects", "Mars Rover Photos"],
        "sub_sections": [
            {"id": "apod", "name": "Astronomy Picture of the Day"},
            {"id": "neo", "name": "Near Earth Objects"},
            {"id": "mars", "name": "Mars Rover Photos"},
        ],
        "has_search": False,
        "auth_required": False,
        "base_url": "https://api.nasa.gov",
        "data_categories": ["Space", "Science", "Imagery"]
    }
