import os

API_CONFIG = {
    "INSURANCE_API": {
        "BASE_URL": os.getenv("INSURANCE_API_BASE", "http://localhost:9000"),
        "API_KEY": os.getenv("INSURANCE_API_KEY", ""),
    },
}

def get_api_info(name: str):
    return API_CONFIG.get(name)
