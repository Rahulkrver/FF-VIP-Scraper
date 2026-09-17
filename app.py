import os
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

# Cloudflare webhook secret
WEBHOOK_SECRET = "RAHULVIP2026"

@app.route('/')
def home():
    return "🚀 VIP Scraper Engine is ALIVE! Go to /scrape to run the engine."

@app.route('/scrape')
def run_scraper():
    print(f"--- Scraping Triggered at {datetime.now()} ---")
    url = "https://www.forexfactory.com/calendar"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        calendar_table = soup.find('table', class_='calendar__table')
        
        events = []
        
        if calendar_table:
            rows = calendar_table.find_all('tr', class_='calendar__row')
            current_date = "Unknown Date"
            
            for row in rows:
                date_cell = row.find('td', class_='calendar__date')
                if date_cell and date_cell.text.strip():
                    current_date = date_cell.text.strip()
                    
                currency_cell = row.find('td', class_='calendar__currency')
                currency = currency_cell.text.strip() if currency_cell else ""
                
                impact_cell = row.find('td', class_='calendar__impact')
                impact = "None"
                if impact_cell:
                    impact_span = impact_cell.find('span')
                    if impact_span and 'icon--ff-impact-red' in impact_span.get('class', []):
                        impact = 'High'
                
                if currency == 'USD' and impact == 'High':
                    event_cell = row.find('td', class_='calendar__event')
                    actual_cell = row.find('td', class_='calendar__actual')
                    forecast_cell = row.find('td', class_='calendar__forecast')
                    previous_cell = row.find('td', class_='calendar__previous')
                    
                    events.append({
                        "date": current_date,
                        "title": event_cell.text.strip() if event_cell else "Unknown Event",
                        "actual": actual_cell.text.strip() if actual_cell else "Pending",
                        "forecast": forecast_cell.text.strip() if forecast_cell else "Awaited",
                        "previous": previous_cell.text.strip() if previous_cell else "Awaited"
                    })
        
        return jsonify({
            "status": "success", 
            "message": "HTML Scraped Successfully",
            "event_count": len(events),
            "data": events
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
