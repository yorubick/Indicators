import json

with open(r"C:\Users\PC\Downloads\poiszn_twitter_dump.json", "r", encoding="utf-8", errors="ignore") as f:
    tweets = json.load(f)

with open(r"C:\Users\PC\.gemini\antigravity\scratch\c_discovery\tweets_full_text.txt", "w", encoding="utf-8") as out:
    for i, tw in enumerate(tweets):
        txt = tw.get("text", "").replace("\n", " ").strip()
        t = tw.get("time", "")[:19]
        u = tw.get("url", "")
        out.write(f"[{i:03d}] {t} | {u}\n      {txt}\n\n")

print(f"Successfully wrote {len(tweets)} tweets to tweets_full_text.txt")
