import os
from flask import Flask, jsonify
import requests
from datetime import datetime
import time

app = Flask(__name__)

WEBHOOK_SECRET = "RAHULVIP2026"

@app.route('/')
def home():
    return "🚀 VIP Scraper Engine is ALIVE! Go to /scrape to run the engine."

@app.route('/scrape')
def run_scraper():
    print(f"--- Scraping Triggered at {datetime.now()} ---")
    
    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
    
    # Pro Browser Headers to avoid 429/403 blocks
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.forexfactory.com/'
    }
    
    try:
        time.sleep(1) # Chota sa natural delay rate limit se bachne ke liye
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 429:
            return jsonify({"status": "error", "message": "Rate limited (429). Please wait a minute and try again."})
            
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
            "message": "JSON Data Fetched Successfully with Referer Header",
            "event_count": len(high_impact_usd),
            "data": high_impact_usd
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
