"""BLS - Bureau of Labor Statistics API Module"""
import requests
import json

BASE_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
HEADERS = {'Content-Type': 'application/json'}

SERIES_MAP = {
    'unemployment': {'id': 'LNS14000000', 'name': 'Unemployment Rate'},
    'cpi': {'id': 'CUUR0000SA0', 'name': 'Consumer Price Index (All Urban)'},
    'employment': {'id': 'CES0000000001', 'name': 'Total Nonfarm Employment'},
    'avg_hourly_earnings': {'id': 'CES0500000003', 'name': 'Average Hourly Earnings'},
}

def get_series_data(series_id, series_name, years=3):
    try:
        import datetime
        end_year = datetime.datetime.now().year
        start_year = end_year - years
        payload = json.dumps({
            "seriesid": [series_id],
            "startyear": str(start_year),
            "endyear": str(end_year)
        })
        resp = requests.post(BASE_URL, data=payload, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            series_data = data.get('Results', {}).get('series', [{}])[0].get('data', [])
            return [{
                'title': f"{series_name}: {d.get('value', '')}",
                'description': f"Period: {d.get('periodName', '')} {d.get('year', '')}",
                'date': f"{d.get('year', '')}-{d.get('period', '').replace('M', '')}-01",
                'link': 'https://www.bls.gov/data/',
                'value': d.get('value', ''),
                'year': d.get('year', ''),
                'period': d.get('periodName', '')
            } for d in series_data]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_bls_data(api_key=None, params=None):
    sub = (params or {}).get('sub_section', 'unemployment')
    series = SERIES_MAP.get(sub, SERIES_MAP['unemployment'])
    return {"results": get_series_data(series['id'], series['name']), "source": "Bureau of Labor Statistics", "endpoint": sub}

def get_metadata():
    return {
        "name": "Bureau of Labor Statistics",
        "acronym": "BLS",
        "description": "Employment, unemployment, CPI, wages, and labor market data",
        "endpoints": ["Unemployment Rate", "CPI", "Total Employment", "Average Hourly Earnings"],
        "sub_sections": [
            {"id": "unemployment", "name": "Unemployment Rate"},
            {"id": "cpi", "name": "Consumer Price Index"},
            {"id": "employment", "name": "Total Nonfarm Employment"},
            {"id": "avg_hourly_earnings", "name": "Average Hourly Earnings"},
        ],
        "has_search": False,
        "auth_required": False,
        "base_url": "https://api.bls.gov",
        "data_categories": ["Economic", "Employment", "Labor"]
    }
