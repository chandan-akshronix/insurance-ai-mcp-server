import requests
from mcp_server.config import get_api_info

def call_api(service_name, path, params=None):
    """Call external API endpoint.
    
    Args:
        service_name: The service name from API_CONFIG (e.g., 'INSURANCE_API')
        path: The API endpoint path (e.g., 'kyc/123456789012')
        params: Optional query parameters
    
    Returns:
        JSON response from the API or error dictionary
    """
    cfg = get_api_info(service_name)
    if not cfg:
        return {"error": f"Service '{service_name}' not configured"}
    
    base = cfg.get("BASE_URL", "").rstrip("/")
    url = f"{base}/{path.lstrip('/')}"
    headers = {}
    
    if cfg.get("API_KEY"):
        headers["x-api-key"] = cfg["API_KEY"]
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}", "url": url}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
