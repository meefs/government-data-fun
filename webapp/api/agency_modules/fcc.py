"""FCC - Federal Communications Commission API Module"""
import requests

HEADERS = {'Accept': 'application/json'}

def get_broadband_data(count=20):
    """Fetch broadband deployment data."""
    try:
        url = "https://broadbandmap.fcc.gov/api/public/map/listMobileAvailabilities"
        # Use the FCC's public API
        url = "https://opendata.fcc.gov/resource/i5zz-k6uu.json?$limit=" + str(count)
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return [{
                'title': r.get('applicant_name', r.get('entity_name', 'Unknown')),
                'description': f"Service: {r.get('service', '')} | State: {r.get('state', '')}",
                'date': r.get('date', r.get('filing_date', '')),
                'link': 'https://broadbandmap.fcc.gov/',
            } for r in data[:count]]
    except Exception:
        pass
    return []

def get_spectrum_licenses(count=20):
    """Fetch spectrum license data."""
    try:
        url = f"https://opendata.fcc.gov/resource/9k46-wbcq.json?$limit={count}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return [{
                'title': r.get('licensee_name', r.get('entity_name', 'Unknown')),
                'description': f"Callsign: {r.get('callsign', '')} | Frequency: {r.get('frequency_assigned', '')} | Service: {r.get('radio_service_desc', '')}",
                'date': r.get('grant_date', ''),
                'link': f"https://wireless2.fcc.gov/UlsApp/UlsSearch/license.jsp",
            } for r in data[:count]]
    except Exception:
        pass
    return []

def get_consumer_complaints(count=20):
    """Fetch FCC consumer complaints."""
    try:
        url = f"https://opendata.fcc.gov/resource/3xyp-aqkj.json?$limit={count}&$order=date_of_issue DESC"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return [{
                'title': r.get('issue', r.get('type_of_issue', 'Complaint')),
                'description': f"Method: {r.get('method', '')} | Status: {r.get('status', '')}",
                'date': r.get('date_of_issue', ''),
                'link': 'https://consumercomplaints.fcc.gov/',
            } for r in data[:count]]
    except Exception:
        pass
    return []

def get_fcc_data(api_key=None, params=None):
    sub = (params or {}).get('sub_section', 'broadband')
    mapping = {
        'broadband': get_broadband_data,
        'spectrum': get_spectrum_licenses,
        'complaints': get_consumer_complaints,
    }
    fn = mapping.get(sub, mapping['broadband'])
    return {"results": fn(), "source": "FCC", "endpoint": sub}

def get_metadata():
    return {
        "name": "Federal Communications Commission",
        "acronym": "FCC",
        "description": "Broadband data, spectrum licenses, and consumer complaints",
        "endpoints": ["Broadband Data", "Spectrum Licenses", "Consumer Complaints"],
        "sub_sections": [
            {"id": "broadband", "name": "Broadband Data"},
            {"id": "spectrum", "name": "Spectrum Licenses"},
            {"id": "complaints", "name": "Consumer Complaints"},
        ],
        "has_search": False,
        "auth_required": False,
        "base_url": "https://opendata.fcc.gov",
        "data_categories": ["Communications", "Broadband", "Spectrum", "Consumer Protection"]
    }
