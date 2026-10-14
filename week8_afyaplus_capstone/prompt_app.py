from __future__ import annotations
import hashlib
from pathlib import Path
from typing import Literal
import yaml
from fastapi import FastAPI
from pydantic import BaseModel

ROOT=Path(__file__).resolve().parent
CFG=yaml.safe_load((ROOT/'config/triage.yaml').read_text())
PROMPT_PATH=ROOT/CFG['prompt_file']
PROMPT_TEXT=PROMPT_PATH.read_text()
PROMPT_SHA=hashlib.sha256(PROMPT_TEXT.encode()).hexdigest()
if PROMPT_SHA != CFG['prompt_sha256']:
    raise RuntimeError('Prompt SHA does not match config pin')

app=FastAPI(title='AfyaPlus Versioned Triage',version=CFG['app_version'])
class TriageRequest(BaseModel):
    text: str
class TriageResponse(BaseModel):
    urgency: Literal['emergency','urgent','routine','self_care']
    rationale: str
    next_step: str
    safety_note: str

def classify(text:str)->dict:
    t=text.lower()
    emergency=('chest pain','cannot breathe','severe breathing','unconscious','uncontrolled bleeding','face droop','slurred speech')
    urgent=('high fever','persistent vomiting','deep cut','worsening pain','pregnant and bleeding')
    selfcare=('mild cold','small scratch','mild headache')
    if any(x in t for x in emergency): u='emergency'; step='Seek emergency care now or call local emergency services.'
    elif any(x in t for x in urgent): u='urgent'; step='Arrange same-day clinical assessment.'
    elif any(x in t for x in selfcare): u='self_care'; step='Use appropriate self-care and monitor for worsening symptoms.'
    else: u='routine'; step='Book a routine clinical consultation.'
    return {'urgency':u,'rationale':'Rule-based, versioned safety classification.','next_step':step,'safety_note':'This service supports triage and does not provide a diagnosis.'}

@app.get('/health')
def health():
    return {'status':'ok','app_version':CFG['app_version'],'model_version':CFG['model_version'],'prompt_version':CFG['prompt_version'],'prompt_sha256':PROMPT_SHA,'mcp_server_version':CFG['mcp_server_version'],'image_tag':CFG['image_tag']}
@app.post('/triage',response_model=TriageResponse)
def triage(req:TriageRequest): return classify(req.text)
