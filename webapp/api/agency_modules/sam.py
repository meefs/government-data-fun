"""SAM.gov - System for Award Management API Module"""
import requests

HEADERS = {'Accept': 'application/json'}

def get_opportunities(count=20, api_key=None):
    """Fetch federal contract opportunities."""
    try:
        key = api_key or ''
        url = f"https://api.sam.gov/opportunities/v2/search?limit={count}&api_key={key}&postedFrom=01/01/2025&postedTo=12/31/2026"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            opps = resp.json().get('opportunitiesData', [])
            return [{
                'title': o.get('title', ''),
                'description': (o.get('description', '') or '')[:300],
                'date': o.get('postedDate', ''),
                'link': o.get('uiLink', f"https://sam.gov/opp/{o.get('noticeId', '')}"),
                'type': o.get('type', ''),
                'department': o.get('department', ''),
                'naics': o.get('naicsCode', '')
            } for o in opps[:count]]
    except Exception as e:
        return [{"error": f"SAM.gov requires API key: {str(e)}"}]
    return []

def get_sam_data(api_key=None, params=None):
    return {"results": get_opportunities(api_key=api_key), "source": "SAM.gov", "endpoint": "Contract Opportunities"}

def get_metadata():
    return {
        "name": "System for Award Management",
        "acronym": "SAM.gov",
        "description": "Federal contract opportunities, entity registrations, and procurement data",
        "endpoints": ["Contract Opportunities"],
        "sub_sections": [
            {"id": "opportunities", "name": "Contract Opportunities"},
        ],
        "has_search": True,
        "search_placeholder": "Search contract opportunities...",
        "auth_required": True,
        "auth_note": "Requires free API key from SAM.gov",
        "base_url": "https://api.sam.gov",
        "data_categories": ["Contracts", "Procurement", "Federal Spending"]
    }
