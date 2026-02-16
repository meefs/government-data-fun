"""DOJ - Department of Justice API Module"""
import requests

BASE_URL = "https://www.justice.gov/api/v1"
HEADERS = {'Accept': 'application/json'}

def fetch_doj(endpoint, count=20):
    try:
        resp = requests.get(f"{BASE_URL}/{endpoint}", params={"pagesize": count}, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            results = resp.json().get('results', [])
            return [{
                'title': r.get('title', r.get('headline', '')),
                'description': (r.get('body', r.get('description', r.get('summary', ''))) or '')[:300],
                'date': r.get('date', r.get('created', r.get('published', ''))),
                'link': r.get('url', r.get('path', '')),
            } for r in results]
    except Exception as e:
        return [{"error": str(e)}]
    return []

def get_doj_data(api_key=None, params=None):
    sub = (params or {}).get('sub_section', 'press_releases')
    mapping = {
        'press_releases': 'press_releases.json',
        'blog_posts': 'blog_posts.json',
        'speeches': 'speeches.json',
        'news': 'news.json',
    }
    endpoint = mapping.get(sub, 'press_releases.json')
    return {"results": fetch_doj(endpoint), "source": "Department of Justice", "endpoint": sub}

def get_metadata():
    return {
        "name": "Department of Justice",
        "acronym": "DOJ",
        "description": "Press releases, news, speeches, and blog posts from the DOJ",
        "endpoints": ["Press Releases", "Blog Posts", "Speeches", "News"],
        "sub_sections": [
            {"id": "press_releases", "name": "Press Releases"},
            {"id": "blog_posts", "name": "Blog Posts"},
            {"id": "speeches", "name": "Speeches"},
            {"id": "news", "name": "News"},
        ],
        "has_search": False,
        "auth_required": False,
        "base_url": "https://www.justice.gov/api/v1",
        "data_categories": ["Legal", "Law Enforcement", "Policy"]
    }
