from __future__ import annotations
import argparse, json
from pathlib import Path
from prompt_app import CFG, classify
ROOT=Path(__file__).resolve().parent

def run(force_failure=False):
    rows=[json.loads(x) for x in (ROOT/'evals/golden.jsonl').read_text().splitlines() if x.strip()]
    passed=0; details=[]
    for i,row in enumerate(rows):
        pred=classify(row['input'])['urgency']
        if force_failure and i==0: pred='routine'
        ok=pred==row['label'] and pred not in row.get('must_not',[])
        passed += int(ok); details.append({'id':row['id'],'expected':row['label'],'predicted':pred,'pass':ok})
    score=passed/len(rows); threshold=float(CFG['eval_threshold'])
    print(json.dumps({'metric':'urgency_agreement','passed':passed,'total':len(rows),'eval_score':score,'threshold':threshold,'details':details},indent=2))
    return 0 if score>=threshold else 1
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--force-failure',action='store_true'); a=p.parse_args(); raise SystemExit(run(a.force_failure))
