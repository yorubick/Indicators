import urllib.request
import json

url = "http://web.archive.org/cdx/search/cdx?url=twitter.com/PoiSzn*&output=json&limit=50"
headers = {"User-Agent": "Mozilla/5.0"}
req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(f"Wayback CDX records: {len(data)}")
        for row in data[:15]:
            print(row[1], row[2])
except Exception as e:
    print("Error:", e)
