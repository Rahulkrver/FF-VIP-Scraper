import os
from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "🔬 Multi-Source Diagnostic Engine is Live! Go to /test to run diagnostics."

@app.route('/test')
def run_diagnostics():
    # Charo sources jo aapne test karne ke liye kahe hain
    urls = {
        "forexfactory": "https://www.forexfactory.com/calendar",
        "investing": "https://in.investing.com/economic-calendar",
        "mql5": "https://www.mql5.com/en/economic-calendar",
        "fmp_api": "https://financialmodelingprep.com/stable/economic-calendar?apikey=61PXtNzBFEDnJmHKnnI99na8vrRS95JB"
    }
    
    # Standard browser headers to bypass basic blocks
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    results = {}
    
    for name, url in urls.items():
        try:
            response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
            
            content_sample = ""
            try:
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    content_sample = response.json()
                else:
                    # HTML ka sirf shuruati sample lenge taaki response clean rahe
                    content_sample = response.text[:300] + "..."
            except Exception:
                content_sample = "Could not parse response body"

            results[name] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "content_type": response.headers.get("Content-Type", "Unknown"),
                "response_sample": content_sample
            }
        except Exception as e:
            results[name] = {
                "status_code": "ERROR",
                "success": False,
                "error": str(e)
            }

    return jsonify({
        "timestamp": str(datetime.now()),
        "diagnostics": results
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
