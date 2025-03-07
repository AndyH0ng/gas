import requests
import json
from const import secrets, config

headers = {
    'Authorization': f'Bearer {secrets.NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2021-05-13'
}

def get_pages(cnt_pages=None):
    url = f'https://api.notion.com/v1/databases/{secrets.DATABASE_ID}/query'
    page_size = config.NOTION_LOAD_SIZE if cnt_pages is None else cnt_pages
    payload = {"page_size": page_size}
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    with open('db.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    results = data['results']
    return results

