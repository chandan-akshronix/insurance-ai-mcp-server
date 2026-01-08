import asyncio
from fastmcp import FastMCP

from mcp_server.tools.application_tool import fetch_application_tool
from mcp_server.tools.kyc_tool import kyc_tool
from mcp_server.tools.credit_tool import credit_tool
from mcp_server.tools.income_tool import income_tool
from mcp_server.tools.medical_tool import medical_tool
from mcp_server.tools.insurance_tool import insurance_history_tool

mcp = FastMCP(name="Insurance-MCP-Server")

@mcp.tool()
async def get_application(pan_number: str) -> dict:
    """Fetch insurance application financial eligibility details using PAN number"""
    return await fetch_application_tool(pan_number)

@mcp.tool()
async def get_kyc(pan_number: str) -> dict:
    """Fetch KYC details using PAN number"""
    return await kyc_tool(pan_number)

@mcp.tool()
async def get_credit(pan_number: str) -> dict:
    """Fetch credit and financial report for applicant"""
    return await credit_tool(pan_number)

@mcp.tool()
async def get_income(pan_number: str) -> dict:
    """Fetch verified income and employment data"""
    return await income_tool(pan_number)

@mcp.tool()
async def get_medical(pan_number: str) -> dict:
    """Fetch applicant's medical and health data"""
    return await medical_tool(pan_number)

@mcp.tool()
async def get_insurance_history(pan_number: str) -> dict:
    """Fetch applicant's past insurance history using PAN number"""
    return await insurance_history_tool(pan_number)

# Create FastAPI app using http_app
app = mcp.http_app()
