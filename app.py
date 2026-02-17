#!/usr/bin/env python3
"""
OpenGovDash Flask Backend - CORS Proxy for Government APIs
Provides endpoints that wrap APIs with strict CORS policies
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='webapp/static', static_url_path='')
CORS(app)

# Create a requests session with proxies disabled
session = requests.Session()
session.trust_env = False  # Disable proxy environment variables completely

# Serve the static HTML file
@app.route('/')
@app.route('/index.html')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/agencies')
def get_agencies():
    """Return list of agencies (frontend will load from HTML)"""
    return jsonify([])

# BLS API proxy
@app.route('/api/bls')
def bls_proxy():
    """Proxy for Bureau of Labor Statistics API"""
    try:
        series = request.args.get('series', 'LNS14000000')
        start_year = request.args.get('start_year', '2021')
        end_year = request.args.get('end_year', '2024')
        limit = int(request.args.get('limit', '20'))

        url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
        payload = {
            'seriesid': [series],
            'startyear': str(start_year),
            'endyear': str(end_year)
        }

        # Bypass proxy for government APIs
        resp = session.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        series_data = (data.get('Results', {}).get('series', [{}])[0].get('data', []))[:limit]

        return jsonify({'status': 'success', 'data': series_data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# USAspending API proxy
@app.route('/api/usaspending', methods=['POST'])
def usaspending_proxy():
    """Proxy for USAspending API"""
    try:
        limit = int(request.args.get('limit', '20'))

        payload = {
            'filters': {},
            'page': 1,
            'limit': limit,
            'sort': '-date_signed'
        }

        url = 'https://api.usaspending.gov/api/v2/search/spending_by_award/'
        resp = session.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        return jsonify({'status': 'success', 'data': data.get('results', [])})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Library of Congress API proxy
@app.route('/api/loc')
def loc_proxy():
    """Proxy for Library of Congress search"""
    try:
        query = request.args.get('q', 'history')
        limit = int(request.args.get('limit', '20'))

        url = f'https://www.loc.gov/search/?q={query}&fo=json&c={limit}'
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# NIH/PubMed proxy
@app.route('/api/nih/pubmed')
def nih_pubmed_proxy():
    """Proxy for NIH PubMed search"""
    try:
        query = request.args.get('q', 'covid')
        limit = int(request.args.get('limit', '20'))
        date_min = request.args.get('date_min', '')

        # Build query with date filter
        q = query
        if date_min:
            year = int(date_min.split('-')[0])
            q += f' AND {year}[PDAT]'

        url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={q}&retmax={limit}&retmode=json&sort=date'
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # Get IDs and fetch summaries
        ids = data.get('esearchresult', {}).get('idlist', [])[:limit]
        if ids:
            summary_url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={",".join(ids)}&retmode=json'
            summary_resp = requests.get(summary_url, timeout=10)
            summary_resp.raise_for_status()
            summary_data = summary_resp.json()
            return jsonify({'status': 'success', 'data': summary_data.get('result', {})})

        return jsonify({'status': 'success', 'data': {}})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# FCC Equipment Authorization proxy
@app.route('/api/fcc/equipment')
def fcc_equipment_proxy():
    """Proxy for FCC Equipment Authorization search"""
    try:
        query = request.args.get('q', '')
        limit = int(request.args.get('limit', '20'))

        # Try Socrata API first
        url = f'https://data.fcc.gov/resource/h994-2nst.json?$limit={limit}'
        if query:
            url += f'&$where=LIKE(prod_name,"%{query}%")'

        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# NIST CVE proxy
@app.route('/api/nist/cves')
def nist_cves_proxy():
    """Proxy for NIST CVE database"""
    try:
        limit = int(request.args.get('limit', '20'))

        url = f'https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage={limit}'
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        return jsonify({'status': 'success', 'data': data.get('vulnerabilities', [])})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# FCC ECFS proxy
@app.route('/api/fcc/ecfs')
def fcc_ecfs_proxy():
    """Proxy for FCC ECFS filings"""
    try:
        query = request.args.get('q', '')
        limit = int(request.args.get('limit', '20'))

        url = f'https://data.fcc.gov/resource/7y7d-n27b.json?$limit={limit}'
        if query:
            url += f'&$where=LIKE(filing_type,"%{query}%")'

        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# DOJ Press Releases proxy
@app.route('/api/doj')
def doj_proxy():
    """Proxy for Department of Justice press releases"""
    try:
        limit = int(request.args.get('limit', '20'))

        url = f'https://www.justice.gov/api/v1/press-releases?pagesize={limit}'
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        return jsonify({'status': 'success', 'data': data.get('results', [])})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# DOT/NHTSA proxy
@app.route('/api/dot/<endpoint>')
def dot_proxy(endpoint):
    """Proxy for DOT/NHTSA recalls and complaints"""
    try:
        limit = int(request.args.get('limit', '20'))

        if endpoint == 'complaints':
            url = f'https://api.nhtsa.gov/complaints?pagesize={limit}&format=json'
        else:  # recalls
            url = f'https://api.nhtsa.gov/recalls/recallsearch?pageindex=0&resultsperpage={limit}&format=json'

        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        return jsonify({'status': 'success', 'data': data.get('results', [])})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# EPA proxy
@app.route('/api/epa')
def epa_proxy():
    """Proxy for EPA environmental data"""
    try:
        sub = request.args.get('sub', 'tri')
        limit = int(request.args.get('limit', '20'))

        base_url = 'https://www.epa.gov/enviro/api/'
        if sub == 'water':
            url = f'{base_url}water_systems/search.json?pagesize={limit}'
        elif sub == 'facilities':
            url = f'{base_url}fii/search.json?pagesize={limit}'
        else:  # toxic releases
            url = f'{base_url}tri/search.json?pagesize={limit}'

        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        return jsonify({'status': 'success', 'data': data if isinstance(data, list) else data.get('results', [])})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# SAM.gov proxy
@app.route('/api/sam')
def sam_proxy():
    """Proxy for SAM.gov contract opportunities"""
    try:
        api_key = request.args.get('key', 'DEMO_KEY')
        limit = int(request.args.get('limit', '20'))
        query = request.args.get('q', '')

        url = f'https://api.sam.gov/opportunities/v2/search?api_key={api_key}&pagesize={limit}'
        if query:
            url += f'&keyword={query}'

        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        return jsonify({'status': 'success', 'data': data.get('opportunitiesData', [])})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# FTC proxy
@app.route('/api/ftc')
def ftc_proxy():
    """Proxy for FTC ReportPortal scam complaints"""
    try:
        limit = int(request.args.get('limit', '20'))

        url = f'https://reportportal.ftc.gov/api/widget/data?pagesize={limit}'
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # Handle different response formats
        results = data if isinstance(data, list) else data.get('data', data.get('reports', []))

        return jsonify({'status': 'success', 'data': results})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# NARA proxy
@app.route('/api/nara')
def nara_proxy():
    """Proxy for National Archives records"""
    try:
        query = request.args.get('q', 'federal government')
        limit = int(request.args.get('limit', '20'))

        url = f'https://catalog.archives.gov/api/v2/records?q={query}&pageSize={limit}'
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        return jsonify({'status': 'success', 'data': data.get('records', [])})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Health check
@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'message': 'OpenGovDash backend is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
