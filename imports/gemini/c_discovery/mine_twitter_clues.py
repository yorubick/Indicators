import json
import re

path = r"C:\Users\PC\Downloads\poiszn_twitter_dump.json"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    tweets = json.load(f)

print(f"Total tweets loaded: {len(tweets)}\n" + "="*60)

keywords = [
    r"\b183\b", r"\b18\.3\b", r"\b72\b", r"\b89\b", r"\b27\b", r"\b45\b", r"\b62\b",
    r"boundary", r"linear", r"window", r"stop", r"growing", r"origin", r"lite",
    r"ema", r"character", r"tree", r"resolution", r"anchor", r"formula", r"math",
    r"code", r"pine", r"script", r"zoom", r"lane", r"seed", r"25%", r"percent",
    r"length", r"period", r"discrete", r"seconds", r"divisor", r"multiplier"
]

pattern = re.compile("|".join(keywords), re.IGNORECASE)

matches = []
for i, tw in enumerate(tweets):
    text = tw.get("text", "")
    time_str = tw.get("time", "")
    url = tw.get("url", "")
    
    found = pattern.findall(text)
    if found:
        unique_matches = sorted(list(set(k.lower() for k in found)))
        matches.append({
            "index": i,
            "time": time_str,
            "url": url,
            "text": text,
            "keywords": unique_matches
        })

print(f"Tweets matching keywords: {len(matches)} / {len(tweets)}\n")

for m in matches:
    print(f"--- [Tweet #{m['index']}] Time: {m['time']} | Matched: {m['keywords']} ---")
    print(f"URL: {m['url']}")
    print(m['text'].strip())
    print("-" * 60)
