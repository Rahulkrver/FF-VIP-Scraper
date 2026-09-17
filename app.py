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
    
    # Using alternative stable economic data feed mirror
    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
    
    # Advanced headers to spoof a real residential browser and bypass cloud firewalls
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://www.forexfactory.com',
        'Referer': 'https://www.forexfactory.com/',
        'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site'
    }
    
    try:
        # Direct request with spoofed browser identity
        response = requests.get(url, headers=headers, timeout=25)
        
        if response.status_code == 429:
            return jsonify({
                "status": "error", 
                "message": "Cloud IP Rate-Limited by Forex Factory CDN. Switching to backup structure soon."
            }), 429
            
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
            "message": "Data Fetched Successfully via Cloud Bypass",
            "event_count": len(high_impact_usd),
            "data": high_impact_usd
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
