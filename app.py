import os
import logging
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smartworld_news")

# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Environment variables
NEWS_API_KEY = os.getenv("60fd4da6f6804c968a27999e80f50449", "").strip()
# Optional: OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

@app.route("/", methods=["GET"])
def index():
    # Serves templates/index.html
    return render_template("index.html")

@app.route("/api/news", methods=["GET"])
def api_news():
    """
    GET /api/news?topic=bitcoin
    Returns JSON: { "articles": [ { "source": "", "title": "", "summary": "", "url": "" }, ... ] }
    """
    topic = request.args.get("topic") or request.args.get("q") or "technology"
    topic = topic.strip() or "technology"

    # If no NewsAPI key provided, return a small demo payload so frontend works immediately
    if not NEWS_API_KEY:
        logger.info("NEWS_API_KEY not set - returning demo article")
        demo = [
            {
                "source": "Demo Source",
                "title": "Welcome to SmartWorld News (Demo)",
                "summary": "Add a NEWS_API_KEY in environment to fetch live news from NewsAPI.org",
                "url": "https://newsapi.org/"
            }
        ]
        return jsonify({"articles": demo})

    # Call NewsAPI
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": NEWS_API_KEY
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
    except requests.RequestException as e:
        logger.exception("Network error when calling NewsAPI")
        return jsonify({"error": "Network error when contacting news provider", "details": str(e), "articles": []}), 502

    # Parse response
    try:
        data = resp.json()
    except ValueError:
        logger.error("Invalid JSON from NewsAPI (status_code=%s)", resp.status_code)
        return jsonify({"error": "Invalid response from news provider", "status_code": resp.status_code, "articles": []}), 502

    # NewsAPI error
    if resp.status_code != 200 or data.get("status") != "ok":
        msg = data.get("message") or data.get("error") or "Unknown NewsAPI error"
        logger.error("NewsAPI returned error: %s (status_code=%s)", msg, resp.status_code)
        return jsonify({"error": msg, "status_code": resp.status_code, "articles": []}), 502

    # Build normalized article list for frontend
    articles = []
    for item in data.get("articles", []):
        try:
            source = (item.get("source") or {}).get("name") or ""
            title = item.get("title") or ""
            summary = item.get("description") or item.get("content") or ""
            url_link = item.get("url") or ""
            articles.append({
                "source": source,
                "title": title,
                "summary": summary,
                "url": url_link
            })
        except Exception:
            # skip problematic entry but continue
            logger.exception("Error processing an article item; skipping")

    return jsonify({"articles": articles})

# Simple health/debug route
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "news_api_key_present": bool(NEWS_API_KEY)})

if __name__ == "__main__":
    # Use dynamic PORT for hosting providers; default to 8080 locally
    port = int(os.environ.get("PORT", 8080))
    logger.info("Starting SmartWorld News on port %s (NEWS_API_KEY set=%s)", port, bool(NEWS_API_KEY))
    app.run(host="0.0.0.0", port=port)
