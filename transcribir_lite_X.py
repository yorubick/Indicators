"""Transcripción local de la guía pública compartida por el usuario."""
import json
import os
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'.tools'/'asr'))
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'
os.environ['HF_HUB_OFFLINE'] = '1'
from faster_whisper import WhisperModel
import numpy as np

model_dir = next((ROOT/'.tools'/'modelos_asr'/'models--Systran--faster-whisper-base.en'/'snapshots').iterdir())
model = WhisperModel(str(model_dir), device='cpu', compute_type='int8', cpu_threads=4)
with wave.open(str(Path(__file__).with_name('Lite_X_2110110293837652362_audio.wav')), 'rb') as audio_file:
    assert audio_file.getframerate() == 16000 and audio_file.getnchannels() == 1
    audio = np.frombuffer(audio_file.readframes(audio_file.getnframes()), dtype=np.int16).astype(np.float32)/32768
segments, _ = model.transcribe(audio, language='en', beam_size=5, vad_filter=True)
out = []
destination = Path(__file__).with_name('Lite_X_2110110293837652362_transcripcion.json')
for segment in segments:
    out.append({'start': segment.start, 'end': segment.end, 'text': segment.text})
    destination.write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(f'{segment.start:.1f}-{segment.end:.1f}: {segment.text}', flush=True)
destination.with_suffix('.txt').write_text('\n'.join(
    f"{s['start']:.1f}-{s['end']:.1f}: {s['text']}" for s in out), encoding='utf-8')
