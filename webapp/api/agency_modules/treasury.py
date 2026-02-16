"""US Treasury - Fiscal Data API Module"""
import requests

BASE_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"
HEADERS = {'Accept': 'application/json'}

def fetch_endpoint(endpoint, params=None, count=20):
    url = f"{BASE_URL}/{endpoint}"
    default_params = {"page[size]": count, "sort": "-record_date"}
    if params:
        default_params.update(params)
    try:
        resp = requests.get(url, params=default_params, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            return resp.json().get('data', [])
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_national_debt(count=20):
    results = fetch_endpoint("v2/accounting/od/debt_to_penny", count=count)
    return [{
        'title': f"Total Public Debt: ${r.get('tot_pub_debt_out_amt', 'N/A')}",
        'description': f"Debt held by public: ${r.get('debt_held_public_amt', 'N/A')} | Intragovt: ${r.get('intragov_hold_amt', 'N/A')}",
        'date': r.get('record_date', ''),
        'link': 'https://fiscaldata.treasury.gov/datasets/debt-to-the-penny/',
        'amount': r.get('tot_pub_debt_out_amt', '')
    } for r in results]

def get_treasury_statements(count=20):
    results = fetch_endpoint("v1/accounting/dts/dts_table_1", count=count)
    return [{
        'title': f"{r.get('account_type', '')} - {r.get('classification_desc', '')}",
        'description': f"Today: ${r.get('today_amt', 'N/A')} | MTD: ${r.get('mtd_amt', 'N/A')} | FYTD: ${r.get('fytd_amt', 'N/A')}",
        'date': r.get('record_date', ''),
        'link': 'https://fiscaldata.treasury.gov/datasets/daily-treasury-statement/',
    } for r in results]

def get_interest_rates(count=20):
    results = fetch_endpoint("v2/accounting/od/avg_interest_rates", count=count)
    return [{
        'title': f"{r.get('security_desc', '')}",
        'description': f"Avg Interest Rate: {r.get('avg_interest_rate_amt', '')}%",
        'date': r.get('record_date', ''),
        'link': 'https://fiscaldata.treasury.gov/datasets/average-interest-rates-treasury-securities/',
        'rate': r.get('avg_interest_rate_amt', '')
    } for r in results]

def get_exchange_rates(count=20):
    results = fetch_endpoint("v1/accounting/od/rates_of_exchange", count=count)
    return [{
        'title': f"{r.get('country', '')} ({r.get('currency', '')})",
        'description': f"Exchange Rate: {r.get('exchange_rate', '')} per USD",
        'date': r.get('record_date', ''),
        'link': 'https://fiscaldata.treasury.gov/datasets/treasury-reporting-rates-exchange/',
    } for r in results]

def get_treasury_data(api_key=None, params=None):
    sub = (params or {}).get('sub_section', 'national_debt')
    mapping = {
        'national_debt': get_national_debt,
        'daily_statements': get_treasury_statements,
        'interest_rates': get_interest_rates,
        'exchange_rates': get_exchange_rates,
    }
    fn = mapping.get(sub, mapping['national_debt'])
    return {"results": fn(), "source": "US Treasury Fiscal Data", "endpoint": sub}

def get_metadata():
    return {
        "name": "US Treasury",
        "acronym": "Treasury",
        "description": "Federal debt, daily treasury statements, interest rates, and exchange rates",
        "endpoints": ["National Debt", "Daily Statements", "Interest Rates", "Exchange Rates"],
        "sub_sections": [
            {"id": "national_debt", "name": "National Debt"},
            {"id": "daily_statements", "name": "Daily Treasury Statements"},
            {"id": "interest_rates", "name": "Average Interest Rates"},
            {"id": "exchange_rates", "name": "Exchange Rates"},
        ],
        "has_search": False,
        "auth_required": False,
        "base_url": "https://api.fiscaldata.treasury.gov",
        "data_categories": ["Financial", "Economic", "Fiscal Policy"]
    }
