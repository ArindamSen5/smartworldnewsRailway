from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import feedparser

app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/news")
def news():
    topic = request.args.get("topic", "technology").strip()
    rss_url = f"https://news.google.com/rss/search?q={topic}+technology&hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(rss_url)

    if not feed.entries:
        return jsonify({
            "articles": [{
                "source": "SmartWorld Demo",
                "title": "No results found.",
                "summary": f"No news available for '{topic}'. Try another keyword.",
                "url": "https://news.google.com/",
                "published": ""
            }]
        })

    articles = []
    for entry in feed.entries[:10]:
        articles.append({
            "source": "Google News",
            "title": entry.title,
            "summary": getattr(entry, "summary", ""),
            "url": entry.link,
            "published": getattr(entry, "published", "")
        })

    return jsonify({"articles": articles})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
