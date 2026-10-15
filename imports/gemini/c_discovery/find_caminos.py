import json

transcript_path = r"C:\Users\PC\.gemini\antigravity\brain\59615641-7193-4fb9-9643-6d4fc1a446d4\.system_generated\logs\transcript.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        content = data.get("content", "")
        # Look for model responses mentioning "Camino 2" or "Solución" or "opciones"
        if ("Camino 2" in content or "camino 2" in content or "Solución B" in content or "tres caminos" in content or "las otras dos soluciones" in content):
            step = data.get("step_index")
            source = data.get("source")
            print(f"Step {step} [{source}]:\n{content[:500]}\n{'-'*60}")
