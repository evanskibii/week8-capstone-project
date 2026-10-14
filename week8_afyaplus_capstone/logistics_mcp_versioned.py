from __future__ import annotations
import json, sys
SERVER_VERSION='1.3.0'
TOOLS=[{'name':'check_stock','description':'Check a clinic item stock level','inputSchema':{'type':'object','properties':{'clinic_id':{'type':'string'},'item':{'type':'string'}},'required':['clinic_id','item']}}]

def response(req):
    rid=req.get('id')
    method=req.get('method')
    if method=='initialize':
        result={'protocolVersion':'2025-03-26','capabilities':{'tools':{}},'serverInfo':{'name':'afyaplus-logistics','version':SERVER_VERSION}}
    elif method=='tools/list': result={'tools':TOOLS}
    elif method=='tools/call':
        p=req.get('params',{}); name=p.get('name'); args=p.get('arguments',{})
        if name!='check_stock': return {'jsonrpc':'2.0','id':rid,'error':{'code':-32601,'message':'Unknown tool'}}
        result={'content':[{'type':'text','text':json.dumps({'clinic_id':args.get('clinic_id'),'item':args.get('item'),'available':True,'quantity':24})}]}
    else: return {'jsonrpc':'2.0','id':rid,'error':{'code':-32601,'message':'Method not found'}}
    return {'jsonrpc':'2.0','id':rid,'result':result}
for line in sys.stdin:
    try: print(json.dumps(response(json.loads(line))),flush=True)
    except Exception as e: print(json.dumps({'jsonrpc':'2.0','id':None,'error':{'code':-32603,'message':str(e)}}),flush=True)
