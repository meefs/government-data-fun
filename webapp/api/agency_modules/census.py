"""Census Bureau API Module"""
import requests

BASE_URL = "https://api.census.gov/data"
HEADERS = {'Accept': 'application/json'}

def get_population_estimates(count=20):
    """Get population estimates by state."""
    try:
        url = f"{BASE_URL}/2023/pep/population?get=NAME,POP_2023,DENSITY_2023&for=state:*"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            header = data[0]
            rows = data[1:]
            return [{
                'title': r[0],
                'description': f"Population: {int(r[1]):,}" if r[1] else "Population: N/A",
                'date': '2023',
                'link': f"https://data.census.gov/",
                'population': r[1],
                'density': r[2] if len(r) > 2 else ''
            } for r in sorted(rows, key=lambda x: int(x[1] or 0), reverse=True)[:count]]
    except Exception:
        pass
    # Fallback to 2022 ACS
    try:
        url = f"{BASE_URL}/2022/acs/acs1?get=NAME,B01001_001E&for=state:*"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            rows = data[1:]
            return [{
                'title': r[0],
                'description': f"Population (ACS 2022): {int(r[1]):,}" if r[1] else "N/A",
                'date': '2022',
                'link': 'https://data.census.gov/',
                'population': r[1]
            } for r in sorted(rows, key=lambda x: int(x[1] or 0), reverse=True)[:count]]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_income_data(count=20):
    """Get median household income by state."""
    try:
        url = f"{BASE_URL}/2022/acs/acs1?get=NAME,B19013_001E&for=state:*"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            rows = data[1:]
            return [{
                'title': r[0],
                'description': f"Median Household Income: ${int(r[1]):,}" if r[1] and r[1] != '-666666666' else "Data not available",
                'date': '2022 ACS',
                'link': 'https://data.census.gov/',
                'income': r[1]
            } for r in sorted(rows, key=lambda x: int(x[1]) if x[1] and x[1] != '-666666666' else 0, reverse=True)[:count]]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_census_data(api_key=None, params=None):
    sub = (params or {}).get('sub_section', 'population')
    mapping = {
        'population': get_population_estimates,
        'income': get_income_data,
    }
    fn = mapping.get(sub, mapping['population'])
    return {"results": fn(), "source": "US Census Bureau", "endpoint": sub}

def get_metadata():
    return {
        "name": "US Census Bureau",
        "acronym": "Census",
        "description": "Population estimates, demographics, income data, and American Community Survey results",
        "endpoints": ["Population Estimates", "Median Income by State"],
        "sub_sections": [
            {"id": "population", "name": "Population by State"},
            {"id": "income", "name": "Median Income by State"},
        ],
        "has_search": False,
        "auth_required": False,
        "base_url": "https://api.census.gov",
        "data_categories": ["Demographics", "Economic", "Population"]
    }
