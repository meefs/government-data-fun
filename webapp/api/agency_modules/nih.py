"""NIH - National Institutes of Health / NLM API Module"""
import requests

HEADERS = {'Accept': 'application/json'}

def get_clinical_trials(count=20, query=None):
    try:
        url = "https://clinicaltrials.gov/api/v2/studies"
        params = {"pageSize": count, "sort": "LastUpdatePostDate:desc"}
        if query:
            params["query.term"] = query
        resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            studies = resp.json().get('studies', [])
            return [{
                'title': s.get('protocolSection', {}).get('identificationModule', {}).get('briefTitle', ''),
                'description': (s.get('protocolSection', {}).get('descriptionModule', {}).get('briefSummary', '') or '')[:300],
                'date': s.get('protocolSection', {}).get('statusModule', {}).get('lastUpdateSubmitDate', ''),
                'link': f"https://clinicaltrials.gov/study/{s.get('protocolSection', {}).get('identificationModule', {}).get('nctId', '')}",
                'status': s.get('protocolSection', {}).get('statusModule', {}).get('overallStatus', ''),
                'phase': ', '.join(s.get('protocolSection', {}).get('designModule', {}).get('phases', []))
            } for s in studies]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_pubmed(count=10, query="health"):
    try:
        search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmax={count}&retmode=json&sort=date"
        resp = requests.get(search_url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            ids = resp.json().get('esearchresult', {}).get('idlist', [])
            if ids:
                id_str = ','.join(ids)
                summary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={id_str}&retmode=json"
                resp2 = requests.get(summary_url, headers=HEADERS, timeout=15)
                if resp2.status_code == 200:
                    result = resp2.json().get('result', {})
                    articles = []
                    for uid in ids:
                        article = result.get(uid, {})
                        if isinstance(article, dict) and 'title' in article:
                            articles.append({
                                'title': article.get('title', ''),
                                'description': f"Authors: {', '.join([a.get('name', '') for a in article.get('authors', [])[:3]])} | Journal: {article.get('source', '')}",
                                'date': article.get('pubdate', ''),
                                'link': f"https://pubmed.ncbi.nlm.nih.gov/{uid}/",
                            })
                    return articles
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_nih_data(api_key=None, params=None):
    sub = (params or {}).get('sub_section', 'clinical_trials')
    query = (params or {}).get('query', '')
    mapping = {
        'clinical_trials': lambda: get_clinical_trials(query=query),
        'pubmed': lambda: get_pubmed(query=query or 'health'),
    }
    fn = mapping.get(sub, mapping['clinical_trials'])
    return {"results": fn(), "source": "NIH/NLM", "endpoint": sub}

def get_metadata():
    return {
        "name": "National Institutes of Health",
        "acronym": "NIH",
        "description": "Clinical trials, PubMed research articles, and biomedical data",
        "endpoints": ["Clinical Trials", "PubMed Articles"],
        "sub_sections": [
            {"id": "clinical_trials", "name": "Clinical Trials"},
            {"id": "pubmed", "name": "PubMed Research"},
        ],
        "has_search": True,
        "search_placeholder": "Search clinical trials or research...",
        "auth_required": False,
        "base_url": "https://clinicaltrials.gov/api",
        "data_categories": ["Health", "Medical Research", "Clinical Trials", "Biomedical"]
    }
