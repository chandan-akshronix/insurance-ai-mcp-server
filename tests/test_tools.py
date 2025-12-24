#!/usr/bin/env python3
"""Simple test harness to exercise MCP tool functions locally.

Run this after starting the FastAPI server (`api.py`) and the MCP server (`server.py`),
and after seeding MongoDB using `mongodb.py`.

Usage:
  python -m tests.test_tools
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Default to local API if not set
os.environ.setdefault("INSURANCE_API_BASE", os.getenv("INSURANCE_API_BASE", "http://localhost:8000"))

from mcp_server.tools.kyc_tool import kyc_tool
from mcp_server.tools.application_tool import fetch_application_tool
from mcp_server.tools.credit_tool import credit_tool
from mcp_server.tools.income_tool import income_tool
from mcp_server.tools.medical_tool import medical_tool
from mcp_server.tools.insurance_tool import insurance_history_tool


def run_tests(pan="AAAPK1234A"):
    print("Testing tools against INSURANCE_API_BASE=", os.environ.get("INSURANCE_API_BASE"))

    try:
        print("\n== KYC ==")
        print(kyc_tool(pan))
    except Exception as e:
        print("KYC call failed:", e)

    try:
        print("\n== Financial Eligibility ==")
        print(fetch_application_tool(pan))
    except Exception as e:
        print("Financial eligibility call failed:", e)

    try:
        print("\n== Credit ==")
        print(credit_tool(pan))
    except Exception as e:
        print("Credit call failed:", e)

    try:
        print("\n== Income ==")
        print(income_tool(pan))
    except Exception as e:
        print("Income call failed:", e)

    try:
        print("\n== Medical ==")
        print(medical_tool(pan))
    except Exception as e:
        print("Medical call failed:", e)

    try:
        print("\n== Insurance History ==")
        print(insurance_history_tool(pan))
    except Exception as e:
        print("Insurance history call failed:", e)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--pan", default=os.getenv("TEST_PAN", "AAAPK1234A"), help="PAN number to test with")
    args = parser.parse_args()
    run_tests(args.pan)
