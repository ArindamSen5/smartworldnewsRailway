from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import feedparser

app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route("/")
def index():
    # Renders your index.html that will auto-load the latest tech news
    return render_template("index.html")

@app.route("/api/news")
def news():
    # Always fetch the latest Technology news
    topic = "technology"
    rss_url = "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(rss_url)

    if not feed.entries:
        return jsonify({
            "articles": [{
                "source": "SmartWorld Demo",
                "title": "No technology news found right now.",
                "summary": "Try again later.",
                "url": "https://news.google.com/",
                "published": ""
            }]
        })

    articles = []
    for entry in feed.entries[:10]:  # Fetch top 10 latest tech stories
        articles.append({
            "source": "Google News",
            "title": entry.title,
            "summary": getattr(entry, "summary", ""),
            "url": entry.link,
            "published": getattr(entry, "published", "")
        })

    return jsonify({"articles": articles})


if __name__ == "__main__":
    # Run Flask app in debug mode (turn off debug=True in production)
    app.run(debug=True, host="0.0.0.0", port=5000)
