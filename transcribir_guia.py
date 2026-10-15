"""Transcripcion local; el video no se envia a ningun servicio externo."""
import os,sys,json,wave
from pathlib import Path
root=Path(__file__).resolve().parents[2]
prefix='auto_zoom' if len(sys.argv)>1 and sys.argv[1]=='auto_zoom' else 'character'
sys.path.insert(0,str(root/'.tools'/'asr'))
os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
os.environ['HF_HUB_DISABLE_XET']='1'
from faster_whisper import WhisperModel
import numpy as np
model_dir=next((root/'.tools'/'modelos_asr'/'models--Systran--faster-whisper-base.en'/'snapshots').iterdir())
model=WhisperModel(str(model_dir),device='cpu',compute_type='int8',cpu_threads=4)
with wave.open(str(Path(__file__).with_name(prefix+'_audio.wav')),'rb') as f:
    assert f.getframerate()==16000 and f.getnchannels()==1
    audio=np.frombuffer(f.readframes(f.getnframes()),dtype=np.int16).astype(np.float32)/32768
segments,info=model.transcribe(audio,
                               language='en',beam_size=5,vad_filter=True)
out=[]
destination=Path(__file__).with_name(prefix+'_transcripcion_automatica.json')
for s in segments:
    item={'start':s.start,'end':s.end,'text':s.text}
    out.append(item)
    destination.write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(f'{s.start:.1f}-{s.end:.1f}: {s.text}',flush=True)
Path(__file__).with_name(prefix+'_transcripcion_automatica.txt').write_text(
    '\n'.join(f"{s['start']:.1f}-{s['end']:.1f}: {s['text']}"for s in out),encoding='utf-8')
