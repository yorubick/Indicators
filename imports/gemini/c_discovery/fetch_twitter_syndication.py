import urllib.request
import json
import re

url = "https://syndication.twitter.com/srv/timeline-profile/screen-name/PoiSzn"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode('utf-8')
        print(f"Success! Fetched {len(html)} bytes.")
        # Save to scratch to inspect
        with open(r'C:\Users\PC\.gemini\antigravity\scratch\c_discovery\syndication_poiszn.html', 'w', encoding='utf-8') as f:
            f.write(html)
        # Look for script tag with data
        match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', html)
        if match:
            data = json.loads(match.group(1))
            print("Found __NEXT_DATA__! Keys:", list(data.keys()))
            with open(r'C:\Users\PC\.gemini\antigravity\scratch\c_discovery\syndication_poiszn.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
except Exception as e:
    print("Error:", e)
