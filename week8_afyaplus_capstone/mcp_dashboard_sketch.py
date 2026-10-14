from tool_metrics import snapshot
def render_text_dashboard():
    rows=snapshot(); return '\n'.join(f'{k} {v}' for k,v in sorted(rows.items())) or 'No tool calls recorded.'
if __name__=='__main__': print(render_text_dashboard())
