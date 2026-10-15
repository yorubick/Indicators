import json

with open(r"C:\Users\PC\Downloads\poiszn_twitter_dump.json", "r", encoding="utf-8") as f:
    tweets = json.load(f)

poiszn_tweets = [t for t in tweets if "/PoiSzn/" in t.get("url", "")]

with open(r"C:\Users\PC\.gemini\antigravity\scratch\c_discovery\poiszn_authored.txt", "w", encoding="utf-8") as out:
    out.write(f"Total PoiSzn tweets: {len(poiszn_tweets)}\n\n")
    for i, t in enumerate(poiszn_tweets):
        out.write(f"=== [{i:02d}] {t['time']} | {t['url']} ===\n")
        out.write(t['text'].strip() + "\n\n")

print(f"Exported {len(poiszn_tweets)} tweets authored by PoiSzn.")
