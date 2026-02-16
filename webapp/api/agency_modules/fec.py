"""FEC - Federal Election Commission API Module"""
import requests

BASE_URL = "https://api.open.fec.gov/v1"
DEMO_KEY = "DEMO_KEY"
HEADERS = {'Accept': 'application/json'}

def get_candidates(count=20, api_key=None):
    key = api_key or DEMO_KEY
    try:
        url = f"{BASE_URL}/candidates/?api_key={key}&sort=-receipts&per_page={count}&election_year=2024"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            results = resp.json().get('results', [])
            return [{
                'title': r.get('name', ''),
                'description': f"Party: {r.get('party_full', '')} | Office: {r.get('office_full', '')} | State: {r.get('state', '')}",
                'date': f"Cycle: {r.get('election_years', [''])[0] if r.get('election_years') else ''}",
                'link': f"https://www.fec.gov/data/candidate/{r.get('candidate_id', '')}/",
                'party': r.get('party_full', ''),
                'office': r.get('office_full', ''),
                'candidate_id': r.get('candidate_id', '')
            } for r in results]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_committee_filings(count=20, api_key=None):
    key = api_key or DEMO_KEY
    try:
        url = f"{BASE_URL}/filings/?api_key={key}&per_page={count}&sort=-receipt_date"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            results = resp.json().get('results', [])
            return [{
                'title': r.get('committee_name', ''),
                'description': f"Form: {r.get('form_type', '')} | Receipts: ${r.get('total_receipts', 0):,.0f} | Disbursements: ${r.get('total_disbursements', 0):,.0f}",
                'date': r.get('receipt_date', ''),
                'link': f"https://www.fec.gov/data/committee/{r.get('committee_id', '')}/",
            } for r in results]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_fec_data(api_key=None, params=None):
    sub = (params or {}).get('sub_section', 'candidates')
    mapping = {
        'candidates': lambda: get_candidates(api_key=api_key),
        'filings': lambda: get_committee_filings(api_key=api_key),
    }
    fn = mapping.get(sub, mapping['candidates'])
    return {"results": fn(), "source": "FEC", "endpoint": sub}

def get_metadata():
    return {
        "name": "Federal Election Commission",
        "acronym": "FEC",
        "description": "Campaign finance data, candidate filings, and political committee information",
        "endpoints": ["Candidates", "Committee Filings"],
        "sub_sections": [
            {"id": "candidates", "name": "Candidates (2024)"},
            {"id": "filings", "name": "Committee Filings"},
        ],
        "has_search": False,
        "auth_required": False,
        "base_url": "https://api.open.fec.gov",
        "data_categories": ["Elections", "Campaign Finance", "Political"]
    }
