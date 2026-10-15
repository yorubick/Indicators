import re
from pathlib import Path

path = Path('C:/Users/PC/.gemini/antigravity/brain/0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27/.system_generated/steps/174/content.md')
text = path.read_text(encoding='utf-8')

# Find the full description text
idx = text.find('PoiSzn EMA Origin Lite is a manually anchored')
if idx != -1:
    print(text[idx:idx+4000])
