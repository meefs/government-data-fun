"""FTC - Federal Trade Commission API Module"""
import requests

HEADERS = {'Accept': 'application/json'}

def get_consumer_sentinel(count=20):
    """FTC Consumer Sentinel data (public summary)."""
    try:
        url = f"https://opendata.fcc.gov/resource/3xyp-aqkj.json?$limit={count}"
        # FTC doesn't have a great public API, use their press releases
        url = "https://www.ftc.gov/api/v1/press_releases.json"
        resp = requests.get(url, params={"pagesize": count}, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            results = resp.json().get('results', resp.json() if isinstance(resp.json(), list) else [])
            return [{
                'title': r.get('title', ''),
                'description': (r.get('body', r.get('description', '')) or '')[:300],
                'date': r.get('date', r.get('created', '')),
                'link': r.get('url', r.get('path', '')),
            } for r in results[:count]]
    except Exception:
        pass
    return []

def get_ftc_cases(count=20):
    """FTC enforcement cases."""
    try:
        url = "https://www.ftc.gov/api/v1/cases.json"
        resp = requests.get(url, params={"pagesize": count}, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            results = resp.json().get('results', [])
            return [{
                'title': r.get('title', ''),
                'description': (r.get('body', '') or '')[:300],
                'date': r.get('date', ''),
                'link': r.get('url', ''),
            } for r in results[:count]]
    except Exception:
        pass
    return []

def get_ftc_data(api_key=None, params=None):
    sub = (params or {}).get('sub_section', 'press_releases')
    mapping = {
        'press_releases': get_consumer_sentinel,
        'cases': get_ftc_cases,
    }
    fn = mapping.get(sub, mapping['press_releases'])
    return {"results": fn(), "source": "FTC", "endpoint": sub}

def get_metadata():
    return {
        "name": "Federal Trade Commission",
        "acronym": "FTC",
        "description": "Consumer protection, antitrust enforcement, press releases and cases",
        "endpoints": ["Press Releases", "Enforcement Cases"],
        "sub_sections": [
            {"id": "press_releases", "name": "Press Releases"},
            {"id": "cases", "name": "Enforcement Cases"},
        ],
        "has_search": False,
        "auth_required": False,
        "base_url": "https://www.ftc.gov/api",
        "data_categories": ["Consumer Protection", "Antitrust", "Privacy", "Data Security"]
    }
