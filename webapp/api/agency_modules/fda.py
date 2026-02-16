"""FDA - Food and Drug Administration API Module (openFDA)"""
import requests

BASE_URL = "https://api.fda.gov"
HEADERS = {'Accept': 'application/json'}

def fetch_endpoint(endpoint, params=None, count=20):
    """Generic openFDA endpoint fetcher."""
    url = f"{BASE_URL}/{endpoint}"
    default_params = {"limit": count}
    if params:
        default_params.update(params)
    try:
        resp = requests.get(url, params=default_params, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('results', [])
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_drug_events(count=20, query=None):
    params = {}
    if query:
        params['search'] = f'patient.drug.medicinalproduct:"{query}"'
    results = fetch_endpoint("drug/event.json", params, count)
    formatted = []
    for r in results:
        patient = r.get('patient', {})
        drugs = patient.get('drug', [{}])
        reactions = patient.get('reaction', [{}])
        formatted.append({
            'title': drugs[0].get('medicinalproduct', 'Unknown Drug') if drugs else 'Unknown',
            'description': ', '.join([rx.get('reactionmeddrapt', '') for rx in reactions[:3]]),
            'date': r.get('receivedate', ''),
            'link': f"https://api.fda.gov/drug/event.json?search=safetyreportid:{r.get('safetyreportid', '')}",
            'serious': r.get('serious', ''),
            'report_id': r.get('safetyreportid', '')
        })
    return formatted

def get_drug_recalls(count=20, query=None):
    params = {}
    if query:
        params['search'] = f'reason_for_recall:"{query}"'
    results = fetch_endpoint("drug/enforcement.json", params, count)
    return [{
        'title': r.get('product_description', '')[:100],
        'description': r.get('reason_for_recall', ''),
        'date': r.get('report_date', ''),
        'link': f"https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts",
        'status': r.get('status', ''),
        'classification': r.get('classification', ''),
        'recalling_firm': r.get('recalling_firm', '')
    } for r in results]

def get_device_510k(count=20, query=None):
    params = {}
    if query:
        params['search'] = f'device_name:"{query}"'
    results = fetch_endpoint("device/510k.json", params, count)
    return [{
        'title': r.get('device_name', ''),
        'description': f"Applicant: {r.get('applicant', '')} | Product Code: {r.get('product_code', '')}",
        'date': r.get('decision_date', ''),
        'link': f"https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID={r.get('k_number', '')}",
        'k_number': r.get('k_number', ''),
        'decision': r.get('decision_description', '')
    } for r in results]

def get_device_recalls(count=20):
    results = fetch_endpoint("device/enforcement.json", {}, count)
    return [{
        'title': r.get('product_description', '')[:100],
        'description': r.get('reason_for_recall', ''),
        'date': r.get('report_date', ''),
        'link': 'https://www.fda.gov/medical-devices/medical-device-recalls',
        'classification': r.get('classification', ''),
        'recalling_firm': r.get('recalling_firm', '')
    } for r in results]

def get_food_recalls(count=20):
    results = fetch_endpoint("food/enforcement.json", {}, count)
    return [{
        'title': r.get('product_description', '')[:100],
        'description': r.get('reason_for_recall', ''),
        'date': r.get('report_date', ''),
        'link': 'https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts',
        'classification': r.get('classification', ''),
        'recalling_firm': r.get('recalling_firm', '')
    } for r in results]

def get_fda_data(api_key=None, params=None):
    sub = (params or {}).get('sub_section', 'drug_events')
    query = (params or {}).get('query', '')
    mapping = {
        'drug_events': lambda: get_drug_events(query=query),
        'drug_recalls': lambda: get_drug_recalls(query=query),
        'device_510k': lambda: get_device_510k(query=query),
        'device_recalls': lambda: get_device_recalls(),
        'food_recalls': lambda: get_food_recalls(),
    }
    fn = mapping.get(sub, mapping['drug_events'])
    return {"results": fn(), "source": "openFDA", "endpoint": sub}

def get_metadata():
    return {
        "name": "Food and Drug Administration",
        "acronym": "FDA",
        "description": "Drug adverse events, recalls, 510(k) device clearances, and food safety data",
        "endpoints": ["Drug Adverse Events", "Drug Recalls", "Device 510(k)", "Device Recalls", "Food Recalls"],
        "sub_sections": [
            {"id": "drug_events", "name": "Drug Adverse Events"},
            {"id": "drug_recalls", "name": "Drug Recalls"},
            {"id": "device_510k", "name": "Device 510(k) Clearances"},
            {"id": "device_recalls", "name": "Device Recalls"},
            {"id": "food_recalls", "name": "Food Recalls"},
        ],
        "has_search": True,
        "search_placeholder": "Search drug name, device, or keyword...",
        "auth_required": False,
        "base_url": "https://api.fda.gov",
        "data_categories": ["Health", "Safety", "Medical Devices", "Pharmaceuticals", "Food Safety"]
    }
