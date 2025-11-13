from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import feedparser

app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/news")
def news():
    topic = request.args.get("topic", "technology")
    
    # Google News RSS feed (no API key required)
    rss_url = f"https://news.google.com/rss/search?q={topic}&hl=en-IN&gl=IN&ceid=IN:en"
    
    feed = feedparser.parse(rss_url)
    
    articles = []
    for entry in feed.entries[:10]:  # limit to 10 results
        articles.append({
            "source": entry.get("source", {}).get("title", "Google News"),
            "title": entry.title,
            "summary": entry.get("summary", ""),
            "url": entry.link,
            "published": entry.get("published", "")
        })
    
    return jsonify({"articles": articles})

if __name__ == "__main__":
    app.run(debug=True)
