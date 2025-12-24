from mcp_server.api_client import call_api

def kyc_tool(pan_number: str):
    """Fetch KYC details using PAN number from Insurance Onboarding API."""
    return call_api("INSURANCE_API", f"kyc/{pan_number}")
