"""NARA - National Archives and Records Administration API Module"""
import requests

BASE_URL = "https://catalog.archives.gov/api/v2"
HEADERS = {'Accept': 'application/json'}

def search_records(query="federal", count=20):
    try:
        url = f"{BASE_URL}/records/search"
        params = {"q": query, "limit": count}
        resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            results = resp.json().get('body', {}).get('hits', {}).get('hits', [])
            return [{
                'title': r.get('_source', {}).get('title', ''),
                'description': (r.get('_source', {}).get('scopeAndContentNote', '') or '')[:300],
                'date': r.get('_source', {}).get('inclusiveDates', {}).get('inclusiveStartDate', {}).get('year', ''),
                'link': f"https://catalog.archives.gov/id/{r.get('_id', '')}",
            } for r in results[:count]]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_nara_data(api_key=None, params=None):
    query = (params or {}).get('query', 'federal records')
    return {"results": search_records(query), "source": "National Archives", "endpoint": "Record Search"}

def get_metadata():
    return {
        "name": "National Archives and Records Administration",
        "acronym": "NARA",
        "description": "Historical federal records, documents, and archival materials",
        "endpoints": ["Record Search"],
        "sub_sections": [
            {"id": "records", "name": "Archival Records"},
        ],
        "has_search": True,
        "search_placeholder": "Search historical records...",
        "auth_required": False,
        "base_url": "https://catalog.archives.gov/api/v2",
        "data_categories": ["Historical", "Archives", "Government Records"]
    }
