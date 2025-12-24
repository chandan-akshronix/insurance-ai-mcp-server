from mcp_server.api_client import call_api

def income_tool(pan_number: str):
    """Fetch verified income and employment data from Insurance API."""
    return call_api("INSURANCE_API", f"income/{pan_number}")
