"""SEC - Securities and Exchange Commission API Module"""
import requests

BASE_URL = "https://efts.sec.gov/LATEST/search-index"
EDGAR_FULL_TEXT = "https://efts.sec.gov/LATEST/search-index"
EDGAR_FILINGS = "https://data.sec.gov/submissions"
EDGAR_SEARCH = "https://efts.sec.gov/LATEST/search-index"

HEADERS = {
    'User-Agent': 'OpenGovDash Research Tool 1.0 contact@opengov.dev',
    'Accept': 'application/json'
}

def get_recent_filings(filing_type="8-K", count=20):
    """Fetch recent SEC EDGAR filings via full-text search."""
    url = "https://efts.sec.gov/LATEST/search-index"
    params = {
        "q": "*",
        "dateRange": "custom",
        "forms": filing_type,
        "from": 0,
        "size": count
    }
    try:
        # Use the EDGAR full-text search API
        search_url = f"https://efts.sec.gov/LATEST/search-index?q=%22{filing_type}%22&forms={filing_type}"
        resp = requests.get(search_url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            hits = data.get('hits', {}).get('hits', [])
            results = []
            for hit in hits[:count]:
                src = hit.get('_source', {})
                results.append({
                    'title': src.get('display_names', [''])[0] if src.get('display_names') else src.get('entity_name', ''),
                    'description': f"{filing_type} filing - {src.get('file_description', '')}",
                    'date': src.get('file_date', ''),
                    'link': f"https://www.sec.gov/Archives/edgar/data/{src.get('entity_id', '')}" if src.get('entity_id') else '',
                    'form_type': src.get('form_type', filing_type),
                    'cik': src.get('entity_id', '')
                })
            return results
    except Exception:
        pass

    # Fallback: EDGAR RSS feed
    try:
        import xmltodict
        url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type={filing_type}&count={count}&output=atom"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = xmltodict.parse(resp.content)
            entries = data.get('feed', {}).get('entry', [])
            if not isinstance(entries, list):
                entries = [entries]
            results = []
            for entry in entries:
                link = entry.get('link', {})
                href = link.get('@href', '') if isinstance(link, dict) else ''
                results.append({
                    'title': entry.get('title', ''),
                    'description': entry.get('summary', {}).get('#text', '') if isinstance(entry.get('summary'), dict) else str(entry.get('summary', '')),
                    'date': entry.get('updated', ''),
                    'link': href,
                    'form_type': filing_type,
                    'cik': ''
                })
            return results
    except Exception as e:
        return [{"error": str(e)}]
    return []

def search_company(query, count=10):
    """Search for company filings by name or CIK."""
    url = f"https://efts.sec.gov/LATEST/search-index?q=%22{query}%22&from=0&size={count}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            hits = data.get('hits', {}).get('hits', [])
            return [{"title": h.get('_source', {}).get('entity_name', ''),
                      "description": h.get('_source', {}).get('file_description', ''),
                      "date": h.get('_source', {}).get('file_date', ''),
                      "link": f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company={query}&type=&dateb=&owner=include&count=40&search_text=&action=getcompany",
                      "form_type": h.get('_source', {}).get('form_type', '')}
                     for h in hits]
    except Exception:
        pass
    return []

def get_sec_data(api_key=None, params=None):
    """Main entry: fetch SEC data based on params."""
    sub = (params or {}).get('sub_section', '8-K')
    query = (params or {}).get('query', '')
    if query:
        return {"results": search_company(query), "source": "SEC EDGAR", "endpoint": "Company Search"}
    filing_types = {
        '8-K': '8-K', '10-K': '10-K', '10-Q': '10-Q',
        '13F': '13F-HR', 'S-1': 'S-1', '20-F': '20-F'
    }
    ft = filing_types.get(sub, sub)
    return {"results": get_recent_filings(ft), "source": "SEC EDGAR", "endpoint": f"{ft} Filings"}

def get_metadata():
    return {
        "name": "Securities and Exchange Commission",
        "acronym": "SEC",
        "description": "Corporate filings, financial disclosures, and securities data from EDGAR",
        "endpoints": ["8-K Filings", "10-K Annual Reports", "10-Q Quarterly", "13F Holdings", "S-1 IPO Filings", "Company Search"],
        "sub_sections": [
            {"id": "8-K", "name": "8-K Current Reports"},
            {"id": "10-K", "name": "10-K Annual Reports"},
            {"id": "10-Q", "name": "10-Q Quarterly Reports"},
            {"id": "13F", "name": "13F Holdings"},
            {"id": "S-1", "name": "S-1 IPO Filings"},
        ],
        "has_search": True,
        "search_placeholder": "Search company name or CIK...",
        "auth_required": False,
        "base_url": "https://data.sec.gov",
        "data_categories": ["Financial", "Corporate", "Securities", "Compliance"]
    }
