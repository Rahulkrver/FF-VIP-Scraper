import os
from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

WEBHOOK_SECRET = "RAHULVIP2026"

@app.route('/')
def home():
    return "🚀 VIP Scraper Engine is ALIVE! Go to /scrape to run the engine."

@app.route('/scrape')
def run_scraper():
    print(f"--- Scraping Triggered at {datetime.now()} ---")
    
    # Forex Factory ka official backend JSON feed URL (No 403 Block on Render)
    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        
        high_impact_usd = []
        for event in data:
            if event.get('country') == 'USD' and event.get('impact') == 'High':
                high_impact_usd.append({
                    "date": event.get('date', 'Unknown'),
                    "title": event.get('title', 'Unknown'),
                    "actual": event.get('actual', 'Pending'),
                    "forecast": event.get('forecast', 'Awaited'),
                    "previous": event.get('previous', 'Awaited')
                })
        
        return jsonify({
            "status": "success",
            "message": "JSON Data Fetched Successfully",
            "event_count": len(high_impact_usd),
            "data": high_impact_usd
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
