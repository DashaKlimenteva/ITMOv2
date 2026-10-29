#!/usr/bin/env python
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main() -> int:
    # Paths
    repo_root = Path(__file__).resolve().parents[4]
    venv_py = repo_root / "practices" / "practice_04" / "mcp" / "demo-subscribers-tool" / "venv" / "Scripts" / "python.exe"
    server_py = repo_root / "practices" / "practice_04" / "mcp" / "demo-subscribers-tool" / "server.py"

    if not venv_py.exists():
        print(f"venv python not found: {venv_py}")
        return 2

    params = StdioServerParameters(command=str(venv_py), args=[str(server_py)])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            print("== initialize ==")
            await session.initialize()

            print("\n== tools/list ==")
            tools = await session.list_tools()
            print(tools)

            async def call(arguments: dict):
                res = await session.call_tool("demo_subscribers", arguments)
                print(res)
                return res

            print("\n== tools/call: count ==")
            await call({"action": "count"})

            print("\n== tools/call: add Alice ==")
            await call({"action": "add", "name": "Alice"})

            print("\n== tools/call: unknown ==")
            await call({"action": "unknown"})

            print("\n== tools/call: invalid name ==")
            await call({"action": "add", "name": ""})

    return 0


if __name__ == "__main__":
    rc = asyncio.run(main())
    sys.exit(rc)

