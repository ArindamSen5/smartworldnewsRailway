import os
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

NEWSAPI_KEY ='60fd4da6f6804c968a27999e80f50449'

def fetch_headlines(query='technology', page_size=10):
    if not NEWSAPI_KEY:
        return [{'title': 'Add NEWSAPI_KEY to fetch live headlines.', 'description': 'No API key provided.'}]
    url = 'https://newsapi.org/v2/top-headlines'
    params = {'apiKey': NEWSAPI_KEY, 'q': query, 'pageSize': page_size, 'language': 'en'}
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()
    return data.get('articles', [])

def summarize_text(text):
    if not text:
        return 'No summary available.'
    parts = text.split('.')
    return '. '.join(parts[:2]) + '.'

@app.route('/api/news')
 topic = request.args.get("topic", "technology")
    api_url = f"https://newsapi.org/v2/everything?q={topic}&apiKey='60fd4da6f6804c968a27999e80f50449'"
    r = requests.get(api_url)
    data = r.json()
    return jsonify(data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)
