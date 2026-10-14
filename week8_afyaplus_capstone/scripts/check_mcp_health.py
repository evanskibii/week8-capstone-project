from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rpc(proc,i,method,params=None):
    req={'jsonrpc':'2.0','id':i,'method':method}
    if params is not None: req['params']=params
    proc.stdin.write(json.dumps(req)+'\n'); proc.stdin.flush()
    line=proc.stdout.readline()
    if not line: raise RuntimeError('MCP server returned no response')
    data=json.loads(line)
    if 'error' in data: raise RuntimeError(data['error'])
    return data['result']
def main(expect_tool='check_stock'):
    p=subprocess.Popen([sys.executable,str(ROOT/'logistics_mcp_versioned.py')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    try:
        init=rpc(p,1,'initialize',{'protocolVersion':'2025-03-26','capabilities':{},'clientInfo':{'name':'ci-health','version':'1.0.0'}})
        tools=rpc(p,2,'tools/list')['tools']; names=[x['name'] for x in tools]
        if init['serverInfo']['version']!='1.3.0': raise RuntimeError('Unexpected MCP version')
        if expect_tool not in names: raise RuntimeError(f'Required tool missing: {expect_tool}; got {names}')
        call=rpc(p,3,'tools/call',{'name':expect_tool,'arguments':{'clinic_id':'CLINIC-001','item':'oxygen'}})
        if not call.get('content'): raise RuntimeError('Tool call returned no content')
        print(json.dumps({'status':'healthy','server':init['serverInfo'],'tools':names,'required_tool':expect_tool},indent=2)); return 0
    except Exception as e:
        print(f'MCP HEALTH FAIL: {e}',file=sys.stderr); return 1
    finally: p.terminate(); p.wait(timeout=5)
if __name__=='__main__':
    a=argparse.ArgumentParser(); a.add_argument('--expect-tool',default='check_stock'); x=a.parse_args(); raise SystemExit(main(x.expect_tool))
