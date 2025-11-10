from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Home route (renders the main page if using templates/index.html)
@app.route("/")
def home():
    return render_template("index.html")

# News API route
@app.route("/api/news", methods=["GET"])
def get_news():
    topic = request.args.get("topic", "technology")
    api_key = os.environ.get("60fd4da6f6804c968a27999e80f50449")  # store your key as Railway variable

    if not api_key:
        return jsonify({"error": "Missing NEWS_API_KEY in environment"}), 500

    # Example using NewsAPI
    url = f"https://newsapi.org/v2/everything?q={topic}&language=en&sortBy=publishedAt&apiKey={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        # Format response for frontend
        articles = []
        for article in data.get("articles", []):
            articles.append({
                "title": article.get("title"),
                "url": article.get("url"),
                "summary": article.get("description"),
                "source": article.get("source", {}).get("name")
            })

        return jsonify({"articles": articles})

    except Exception as e:
        print("Error fetching news:", e)
        return jsonify({"error": "Failed to fetch news"}), 500


# Entry point for Railway or local run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
