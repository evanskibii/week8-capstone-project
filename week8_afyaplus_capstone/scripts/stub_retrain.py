from pathlib import Path
import datetime, re, yaml
ROOT=Path(__file__).resolve().parents[1]; p=ROOT/'config/triage.yaml'; cfg=yaml.safe_load(p.read_text())
old=cfg['model_version']; m=re.match(r'(.*?)(\d+)$',old); new=(m.group(1)+str(int(m.group(2))+1)) if m else old+'-stub.1'
cfg['model_version']=new; p.write_text(yaml.safe_dump(cfg,sort_keys=False))
with (ROOT/'CHANGELOG.md').open('a') as f: f.write(f'\n- {datetime.date.today().isoformat()}: simulated retrain only; model_version {old} -> {new}; no weights trained.\n')
print(f'STUB RETRAIN: {old} -> {new}; no weights trained')
