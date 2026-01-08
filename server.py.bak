import asyncio

from fastmcp import FastMCP

from mcp_server.tools.application_tool import fetch_application_tool
from mcp_server.tools.kyc_tool import kyc_tool
from mcp_server.tools.credit_tool import credit_tool
from mcp_server.tools.income_tool import income_tool
from mcp_server.tools.medical_tool import medical_tool
from mcp_server.tools.insurance_tool import insurance_history_tool



TOOLS = [
    (fetch_application_tool, "Fetch insurance application financial eligibility details using PAN number"),
    (kyc_tool, "Fetch KYC details using PAN number"),
    (credit_tool, "Fetch credit and financial report for applicant"),
    (income_tool, "Fetch verified income and employment data"),
    (medical_tool, "Fetch applicant's medical and health data"),
    (insurance_history_tool, "Fetch applicant's past insurance history using PAN number"),
]

mcp = FastMCP(name="Insurance-MCP-Server", host="0.0.0.0", port=7000)

for func, description in TOOLS:
    mcp.add_tool(func, name=func.__name__, description=description)

def run_sse_server():
    """Run the FastMCP server over SSE using uvicorn.run().

    Using the synchronous `uvicorn.run` avoids signal handling issues
    on some Windows Python setups when awaiting `Server.serve()`.
    """
    from starlette.applications import Starlette
    from starlette.routing import Route
    import uvicorn
    from mcp.server.sse import SseServerTransport

    sse = SseServerTransport("/messages")

    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await mcp._mcp_server.run(
                streams[0],
                streams[1],
                mcp._mcp_server.create_initialization_options(),
            )

    async def handle_messages(request):
        await sse.handle_post_message(request.scope, request.receive, request._send)

    starlette_app = Starlette(
        debug=mcp.settings.debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Route("/messages", endpoint=handle_messages, methods=["POST"]),
        ],
    )

    # Use the high-level run API which handles signals cleanly across platforms
    uvicorn.run(
        starlette_app,
        host=mcp.settings.host,
        port=mcp.settings.port,
        log_level=mcp.settings.log_level,
    )

if __name__ == "__main__":
    print(f"Starting Insurance MCP Server on port {mcp.settings.port} ...")
    run_sse_server()
