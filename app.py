from flask import Flask, jsonify, request

import requests
import os

app = Flask(__name__)
CORS(app)

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "demo")

@app.route('/')
def home():
    return jsonify({"message": "SmartWorld News API is running!"})

@app.route('/api/news', methods=['GET'])
def get_news():
    topic = request.args.get('topic', 'technology')

    if NEWS_API_KEY == "demo":
        return jsonify({
            "articles": [
                {
                    "source": "Demo Source",
                    "title": "Welcome to SmartWorld News!",
                    "summary": "Fetch real news by adding your API key.",
                    "url": "https://newsapi.org/"
                }
            ]
        })

    url = f"https://newsapi.org/v2/everything?q={topic}&language=en&sortBy=publishedAt&pageSize=10&apiKey={60fd4da6f6804c968a27999e80f50449}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        articles = []
        if "articles" in data:
            for item in data["articles"]:
                articles.append({
                    "source": item["source"]["name"],
                    "title": item["title"],
                    "summary": item["description"],
                    "url": item["url"]
                })

        return jsonify({"articles": articles})
    except Exception as e:
        retur
