import json

with open(r"C:\Users\PC\Downloads\poiszn_twitter_dump.json", "r", encoding="utf-8") as f:
    tweets = json.load(f)

for i, tw in enumerate(tweets):
    txt = tw.get("text", "")
    t_lower = txt.lower()
    if any(k in t_lower for k in ["youtube", "youtu.be", "whop", "video", "yt", "discord"]):
        print(f"[{i:03d}] {tw.get('url')}\n{txt}\n{'-'*50}")
