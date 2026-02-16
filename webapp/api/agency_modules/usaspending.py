"""USAspending.gov API Module - Federal Spending Data"""
import requests

BASE_URL = "https://api.usaspending.gov/api/v2"
HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}

def get_top_agencies(count=20):
    try:
        url = f"{BASE_URL}/references/toptier_agencies/"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get('results', [])[:count]
            return [{
                'title': r.get('agency_name', ''),
                'description': f"Budget: ${r.get('budget_authority_amount', 0):,.0f} | Obligated: ${r.get('obligated_amount', 0):,.0f}",
                'date': r.get('current_total_budget_authority_amount', ''),
                'link': f"https://www.usaspending.gov/agency/{r.get('agency_slug', '')}",
                'budget': r.get('budget_authority_amount', 0),
                'obligated': r.get('obligated_amount', 0),
                'abbreviation': r.get('abbreviation', '')
            } for r in results]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def search_spending(query, count=20):
    try:
        url = f"{BASE_URL}/search/spending_by_award/"
        payload = {
            "filters": {
                "keywords": [query],
                "time_period": [{"start_date": "2024-01-01", "end_date": "2026-12-31"}]
            },
            "fields": ["Award ID", "Recipient Name", "Award Amount", "Description", "Start Date", "Awarding Agency"],
            "limit": count,
            "page": 1,
            "sort": "Award Amount",
            "order": "desc"
        }
        resp = requests.post(url, json=payload, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return [{
                'title': r.get('Recipient Name', 'Unknown'),
                'description': f"Award: {r.get('Award ID', '')} - {(r.get('Description', '') or '')[:150]}",
                'date': r.get('Start Date', ''),
                'link': f"https://www.usaspending.gov/award/{r.get('internal_id', '')}",
                'amount': r.get('Award Amount', 0),
                'agency': r.get('Awarding Agency', '')
            } for r in data.get('results', [])]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_federal_accounts(count=20):
    try:
        url = f"{BASE_URL}/federal_accounts/"
        payload = {"sort": {"field": "budgetary_resources", "direction": "desc"}, "limit": count, "page": 1}
        resp = requests.post(url, json=payload, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return [{
                'title': r.get('account_name', ''),
                'description': f"Agency: {r.get('managing_agency', '')} | Budget: ${r.get('budgetary_resources', 0):,.0f}",
                'date': '',
                'link': f"https://www.usaspending.gov/federal_account/{r.get('account_number', '')}",
                'budget': r.get('budgetary_resources', 0)
            } for r in data.get('results', [])]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_usaspending_data(api_key=None, params=None):
    sub = (params or {}).get('sub_section', 'top_agencies')
    query = (params or {}).get('query', '')
    if query:
        return {"results": search_spending(query), "source": "USAspending.gov", "endpoint": "Award Search"}
    mapping = {
        'top_agencies': get_top_agencies,
        'federal_accounts': get_federal_accounts,
    }
    fn = mapping.get(sub, mapping['top_agencies'])
    return {"results": fn(), "source": "USAspending.gov", "endpoint": sub}

def get_metadata():
    return {
        "name": "USAspending.gov",
        "acronym": "USAspending",
        "description": "Federal spending, contracts, grants, and budget data across all agencies",
        "endpoints": ["Top Agencies by Budget", "Federal Accounts", "Award Search"],
        "sub_sections": [
            {"id": "top_agencies", "name": "Top Agencies by Budget"},
            {"id": "federal_accounts", "name": "Federal Accounts"},
        ],
        "has_search": True,
        "search_placeholder": "Search contracts, grants, recipients...",
        "auth_required": False,
        "base_url": "https://api.usaspending.gov",
        "data_categories": ["Financial", "Contracts", "Grants", "Federal Spending"]
    }
