"""NIST - National Institute of Standards and Technology (NVD) API Module"""
import requests

BASE_URL = "https://services.nvd.nist.gov/rest/json"
HEADERS = {'Accept': 'application/json'}

def get_recent_cves(count=20):
    """Fetch recent CVE vulnerability records."""
    try:
        url = f"{BASE_URL}/cves/2.0?resultsPerPage={count}"
        resp = requests.get(url, headers=HEADERS, timeout=20)
        if resp.status_code == 200:
            vulns = resp.json().get('vulnerabilities', [])
            results = []
            for v in vulns[:count]:
                cve = v.get('cve', {})
                desc_list = cve.get('descriptions', [])
                desc = next((d.get('value', '') for d in desc_list if d.get('lang') == 'en'), '')
                metrics = cve.get('metrics', {})
                cvss = ''
                if metrics.get('cvssMetricV31'):
                    cvss = metrics['cvssMetricV31'][0].get('cvssData', {}).get('baseScore', '')
                elif metrics.get('cvssMetricV2'):
                    cvss = metrics['cvssMetricV2'][0].get('cvssData', {}).get('baseScore', '')
                results.append({
                    'title': cve.get('id', ''),
                    'description': desc[:300],
                    'date': cve.get('published', ''),
                    'link': f"https://nvd.nist.gov/vuln/detail/{cve.get('id', '')}",
                    'cvss_score': cvss,
                    'source': cve.get('sourceIdentifier', '')
                })
            return results
    except Exception as e:
        return [{"error": str(e)}]
    return []

def search_cves(query, count=20):
    """Search CVEs by keyword."""
    try:
        url = f"{BASE_URL}/cves/2.0?keywordSearch={query}&resultsPerPage={count}"
        resp = requests.get(url, headers=HEADERS, timeout=20)
        if resp.status_code == 200:
            vulns = resp.json().get('vulnerabilities', [])
            results = []
            for v in vulns[:count]:
                cve = v.get('cve', {})
                desc_list = cve.get('descriptions', [])
                desc = next((d.get('value', '') for d in desc_list if d.get('lang') == 'en'), '')
                results.append({
                    'title': cve.get('id', ''),
                    'description': desc[:300],
                    'date': cve.get('published', ''),
                    'link': f"https://nvd.nist.gov/vuln/detail/{cve.get('id', '')}",
                })
            return results
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_nist_data(api_key=None, params=None):
    query = (params or {}).get('query', '')
    if query:
        return {"results": search_cves(query), "source": "NIST NVD", "endpoint": "CVE Search"}
    return {"results": get_recent_cves(), "source": "NIST NVD", "endpoint": "Recent CVEs"}

def get_metadata():
    return {
        "name": "National Institute of Standards and Technology",
        "acronym": "NIST",
        "description": "National Vulnerability Database - CVE records, CVSS scores, and cybersecurity vulnerability data",
        "endpoints": ["Recent CVEs", "CVE Search"],
        "sub_sections": [
            {"id": "recent_cves", "name": "Recent Vulnerabilities"},
        ],
        "has_search": True,
        "search_placeholder": "Search CVEs by keyword (e.g., 'apache', 'windows')...",
        "auth_required": False,
        "base_url": "https://services.nvd.nist.gov",
        "data_categories": ["Cybersecurity", "Vulnerabilities", "Compliance"]
    }
