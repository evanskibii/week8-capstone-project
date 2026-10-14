from scripts.check_mcp_health import main
def test_mcp_health_passes(): assert main('check_stock')==0
def test_mcp_health_fails_closed(): assert main('missing_tool')==1
