from mcp_server.api_client import call_api

def fetch_application_tool(pan_number: str):
    """Fetch insurance application financial eligibility details using PAN number."""
    return call_api("INSURANCE_API", f"financial-eligibility/{pan_number}")
