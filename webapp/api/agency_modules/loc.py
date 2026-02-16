"""LOC - Library of Congress API Module"""
import requests

BASE_URL = "https://www.loc.gov"
HEADERS = {'Accept': 'application/json'}

def search_collections(query="government", count=20):
    try:
        url = f"{BASE_URL}/search/?q={query}&fo=json&c={count}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            results = resp.json().get('results', [])
            return [{
                'title': r.get('title', r.get('description', [''])[0] if isinstance(r.get('description'), list) else ''),
                'description': r.get('description', [''])[0][:300] if isinstance(r.get('description'), list) else (r.get('description', '') or '')[:300],
                'date': r.get('date', ''),
                'link': r.get('url', r.get('id', '')),
            } for r in results[:count]]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_loc_data(api_key=None, params=None):
    query = (params or {}).get('query', 'government')
    return {"results": search_collections(query), "source": "Library of Congress", "endpoint": "Collection Search"}

def get_metadata():
    return {
        "name": "Library of Congress",
        "acronym": "LOC",
        "description": "Digital collections, historical records, and the national library catalog",
        "endpoints": ["Collection Search"],
        "sub_sections": [
            {"id": "collections", "name": "Digital Collections"},
        ],
        "has_search": True,
        "search_placeholder": "Search Library of Congress collections...",
        "auth_required": False,
        "base_url": "https://www.loc.gov",
        "data_categories": ["Historical", "Cultural", "Archives", "Research"]
    }
