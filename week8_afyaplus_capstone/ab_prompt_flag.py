import hashlib, os
STABLE='1.2.0'; CANDIDATE='1.3.0-candidate'
def prompt_for_key(key:str,percent:int|None=None)->str:
    pct=int(os.getenv('CANDIDATE_PERCENT','10')) if percent is None else percent
    bucket=int(hashlib.sha256(key.encode()).hexdigest()[:8],16)%100
    return CANDIDATE if bucket<pct else STABLE
if __name__=='__main__': print(prompt_for_key(os.getenv('STAGING_KEY','demo-key')))
