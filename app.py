from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests, os

app = Flask(__name__, template_folder='templates')
CORS(app)

NEWS_API_KEY = os.getenv("60fd4da6f6804c968a27999e80f50449", "")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/news")
def news():
    topic = request.args.get("topic", "technology")
    if not NEWS_API_KEY:
        return jsonify({
            "articles": [{
                "source": "Demo Source",
                "title": "SmartWorld News demo working!",
                "summary": "Add your NEWS_API_KEY to show live news.",
                "url": "https://newsapi.org/"
            }]
        })
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}"
    res = requests.get(url)
    return jsonify(res.json())
    
if __name__ == "__main__":
    app.run(debug=True)
