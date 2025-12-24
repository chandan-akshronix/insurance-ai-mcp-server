from mcp_server.api_client import call_api

def credit_tool(pan_number: str, bureau: str = "CIBIL"):
    """Fetch credit report for applicant from Insurance API."""
    return call_api("INSURANCE_API", f"credit/{pan_number}", {"bureau": bureau})
