# Insurance MCP Server

This repository contains a standalone MCP (fastmcp) server exposing tools used by the Insurance LangGraph pipeline.
It was generated to mirror and extract the `app/mcp_server` components from the main project.

## Contents
- `server.py` — launches the MCP server on port 8765
- `mcp_server/` — main package with tools, api client and config
- `tests/` — simple unit tests for tools (mocked)

## Quickstart
1. Copy `.env.example` to `.env` and fill API endpoints / keys.
2. `python -m pip install -r requirements.txt` or use `poetry`/`pyproject.toml`.
3. `python server.py` to start the MCP server on port 8765.

## Notes
This server is compatible with the LangGraph agents that call MCPClient in your main project.
