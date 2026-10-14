import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
pin=json.loads((ROOT/'prompts/pin.json').read_text())
p=ROOT/'prompts'/pin['file']
actual=hashlib.sha256(p.read_bytes()).hexdigest()
if actual != pin['sha256']:
    raise SystemExit(f'FAIL prompt pin: expected {pin["sha256"]}, got {actual}')
print(f'PASS prompt_version={pin["prompt_version"]} sha256={actual}')
