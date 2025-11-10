# SmartWorld News - Production Ready

This is the production-ready version of SmartWorld News:

- Gunicorn for production server (no Flask development warning)
- Google AdSense placeholders added
- Ready to deploy on Railway.app or any Python host

## Deploy

1. Go to https://railway.app → New Project → Deploy from GitHub or upload ZIP
2. Add environment variables:
   - NEWSAPI_KEY = your key from https://newsapi.org
   - OPENAI_API_KEY = optional
   - PORT = 8080
3. Deploy → live URL will be provided by Railway
4. Replace AdSense placeholders with your actual publisher ID and ad-slot IDs
