from mcp_server.api_client import call_api

def medical_tool(pan_number: str):
    """Fetch applicant's medical report from Insurance API."""
    return call_api("INSURANCE_API", f"medical/{pan_number}")
