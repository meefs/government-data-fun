"""FDIC - Federal Deposit Insurance Corporation API Module"""
import requests

BASE_URL = "https://banks.data.fdic.gov/api"
HEADERS = {'Accept': 'application/json'}

def get_institutions(count=20):
    try:
        url = f"{BASE_URL}/financials?limit={count}&sort_by=REPDTE&sort_order=DESC"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json().get('data', [])
            return [{
                'title': r.get('data', {}).get('REPNM', r.get('data', {}).get('INSTNAME', '')),
                'description': f"Assets: ${r.get('data', {}).get('ASSET', 0):,.0f}K | Deposits: ${r.get('data', {}).get('DEP', 0):,.0f}K | Equity: ${r.get('data', {}).get('EQ', 0):,.0f}K",
                'date': r.get('data', {}).get('REPDTE', ''),
                'link': f"https://www.fdic.gov/",
                'total_assets': r.get('data', {}).get('ASSET', 0),
            } for r in data]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_failures(count=20):
    try:
        url = f"{BASE_URL}/failures?limit={count}&sort_by=FAILDATE&sort_order=DESC"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json().get('data', [])
            return [{
                'title': r.get('data', {}).get('NAME', ''),
                'description': f"City: {r.get('data', {}).get('CITY', '')}, {r.get('data', {}).get('STATE', '')} | Total Deposits: ${r.get('data', {}).get('TOTALDEPOSITS', 0):,.0f} | Acquiring Institution: {r.get('data', {}).get('ACQUIREDINSTITUTION', '')}",
                'date': r.get('data', {}).get('FAILDATE', ''),
                'link': f"https://www.fdic.gov/resources/resolutions/bank-failures/",
            } for r in data]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_fdic_data(api_key=None, params=None):
    sub = (params or {}).get('sub_section', 'institutions')
    mapping = {
        'institutions': get_institutions,
        'failures': get_failures,
    }
    fn = mapping.get(sub, mapping['institutions'])
    return {"results": fn(), "source": "FDIC", "endpoint": sub}

def get_metadata():
    return {
        "name": "Federal Deposit Insurance Corporation",
        "acronym": "FDIC",
        "description": "Bank financial data, institution information, and bank failure records",
        "endpoints": ["Financial Institutions", "Bank Failures"],
        "sub_sections": [
            {"id": "institutions", "name": "Financial Institutions"},
            {"id": "failures", "name": "Bank Failures"},
        ],
        "has_search": False,
        "auth_required": False,
        "base_url": "https://banks.data.fdic.gov/api",
        "data_categories": ["Financial", "Banking", "Regulatory"]
    }
