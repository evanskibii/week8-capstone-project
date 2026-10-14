from fastapi.testclient import TestClient
from prompt_app import app, CFG, PROMPT_SHA, classify

def test_prompt_pin_matches(): assert PROMPT_SHA==CFG['prompt_sha256']
def test_health_exposes_versions():
    d=TestClient(app).get('/health').json()
    assert d['status']=='ok' and d['prompt_sha256']==PROMPT_SHA and d['mcp_server_version']=='1.3.0'
def test_emergency_rule(): assert classify('cannot breathe with chest pain')['urgency']=='emergency'
def test_triage_schema(): assert TestClient(app).post('/triage',json={'text':'mild cold'}).status_code==200
