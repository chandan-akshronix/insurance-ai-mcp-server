from mcp_server.api_client import call_api

def insurance_history_tool(pan_number: str):
    """Fetch applicant's past insurance history using PAN number."""
    return call_api("INSURANCE_API", f"insurance-history/{pan_number}")
