from collections import Counter
from threading import Lock
_counts=Counter(); _lock=Lock()
def record(tool:str,status:str):
    with _lock: _counts[(tool,status)]+=1
def snapshot():
    with _lock: return {f'{k[0]}:{k[1]}':v for k,v in _counts.items()}
