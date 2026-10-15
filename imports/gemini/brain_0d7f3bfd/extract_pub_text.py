import re
from pathlib import Path

path = Path('C:/Users/PC/.gemini/antigravity/brain/0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27/.system_generated/steps/174/content.md')
text = path.read_text(encoding='utf-8')

# Search for the script description
pattern = re.compile(r'class="[^"]*body-[^"]*"[^>]*>(.*?)</div>', re.DOTALL)
matches = pattern.findall(text)
for m in matches:
    clean = re.sub(r'<[^>]+>', ' ', m).strip()
    if len(clean) > 50:
        print("MATCH:", clean[:1000])

# Search for any text containing "Lite" or "range"
print("\n--- SEARCHING SPECIFIC TERMS ---")
for line in text.splitlines():
    if any(k in line.lower() for k in ['poi', 'origin', 'lite', 'range', 'anchor', 'formula', 'calculation']):
        clean = re.sub(r'<[^>]+>', ' ', line).strip()
        if len(clean) > 40 and not clean.startswith('{') and not clean.startswith('window.'):
            print("LINE:", clean[:300])
