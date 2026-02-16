"""DOT - Department of Transportation API Module"""
import requests

HEADERS = {'Accept': 'application/json'}

def get_airline_stats(count=20):
    """NHTSA vehicle recall data as DOT proxy."""
    try:
        url = f"https://api.nhtsa.gov/recalls/recallsByDate?startDate=2025-01-01&endDate=2026-12-31&limit={count}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            results = resp.json().get('results', [])
            return [{
                'title': f"{r.get('Manufacturer', '')} - {r.get('Subject', '')}",
                'description': (r.get('Summary', '') or '')[:300],
                'date': r.get('ReportReceivedDate', ''),
                'link': f"https://www.nhtsa.gov/recalls",
                'component': r.get('Component', ''),
                'units_affected': r.get('PotentialNumberofUnitsAffected', '')
            } for r in results[:count]]
    except Exception:
        pass
    # Fallback: NHTSA complaints
    try:
        url = f"https://api.nhtsa.gov/complaints?make=toyota&model=camry"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            results = resp.json().get('results', [])[:count]
            return [{
                'title': f"{r.get('make', '')} {r.get('model', '')} ({r.get('modelYear', '')})",
                'description': (r.get('summary', '') or '')[:300],
                'date': r.get('dateOfIncident', ''),
                'link': 'https://www.nhtsa.gov/complaints',
            } for r in results]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_vehicle_recalls(count=20):
    try:
        url = "https://api.nhtsa.gov/recalls/recallsByYear?year=2025"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            results = resp.json().get('results', [])[:count]
            return [{
                'title': f"{r.get('Manufacturer', '')} - {r.get('Subject', '')}",
                'description': (r.get('Summary', '') or '')[:300],
                'date': r.get('ReportReceivedDate', ''),
                'link': f"https://www.nhtsa.gov/recalls",
            } for r in results]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_dot_data(api_key=None, params=None):
    sub = (params or {}).get('sub_section', 'recalls')
    mapping = {
        'recalls': get_vehicle_recalls,
        'complaints': get_airline_stats,
    }
    fn = mapping.get(sub, mapping['recalls'])
    return {"results": fn(), "source": "DOT/NHTSA", "endpoint": sub}

def get_metadata():
    return {
        "name": "Department of Transportation",
        "acronym": "DOT",
        "description": "Vehicle recalls, safety complaints, and transportation safety data via NHTSA",
        "endpoints": ["Vehicle Recalls", "Safety Complaints"],
        "sub_sections": [
            {"id": "recalls", "name": "Vehicle Recalls (2025)"},
            {"id": "complaints", "name": "Safety Complaints"},
        ],
        "has_search": False,
        "auth_required": False,
        "base_url": "https://api.nhtsa.gov",
        "data_categories": ["Transportation", "Safety", "Vehicle Recalls"]
    }
