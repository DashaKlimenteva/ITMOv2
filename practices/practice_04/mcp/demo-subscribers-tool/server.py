#!/usr/bin/env python
"""
MCP stdio server: demo-subscribers

Tools:
  - demo-subscribers: manage an in-memory set of subscribers
    input: {"action": "count"|"clear"|"add", "name"?: str}
    output:
      count -> {"ok": true, "count": N}
      clear -> {"ok": true, "cleared": true}
      add   -> {"ok": true, "added": bool, "name": "normalized"}
      error -> {"ok": false, "error": "unknown_action"|"invalid_name"}
"""
from __future__ import annotations

import asyncio
import json
import re
import sys
from typing import Any, Dict

try:
    # Explicit import for MCP 2.x
    from mcp.server.mcpserver import MCPServer
except Exception:
    MCPServer = None  # type: ignore


def normalize_name(name: str) -> str:
    # trim + collapse spaces + lower
    s = name.strip()
    s = re.sub(r"\s+", " ", s)
    return s.lower()


class InMemorySubscribers:
    def __init__(self) -> None:
        self._set: set[str] = set()

    def count(self) -> int:
        return len(self._set)

    def clear(self) -> None:
        self._set.clear()

    def add(self, name: str) -> bool:
        n = normalize_name(name)
        if not n:
            raise ValueError("invalid_name")
        before = len(self._set)
        self._set.add(n)
        return len(self._set) > before


subscribers = InMemorySubscribers()


async def main() -> int:
    if MCPServer is None:
        print("MCP SDK (mcp) is not installed. Install with: pip install mcp", file=sys.stderr)
        return 2

    mcp = MCPServer("demo-subscribers")

    @mcp.tool()
    def demo_subscribers(action: str, name: str | None = None) -> Dict[str, Any]:
        """Manage subscribers. action: count|clear|add."""
        try:
            if action == "count":
                return {"ok": True, "count": subscribers.count()}
            elif action == "clear":
                subscribers.clear()
                return {"ok": True, "cleared": True}
            elif action == "add":
                if name is None or not name.strip():
                    return {"ok": False, "error": "invalid_name"}
                added = subscribers.add(name)
                return {"ok": True, "added": added, "name": normalize_name(name)}
            else:
                return {"ok": False, "error": "unknown_action"}
        except ValueError as ve:
            if str(ve) == "invalid_name":
                return {"ok": False, "error": "invalid_name"}
            return {"ok": False, "error": "internal", "details": str(ve)}
        except Exception as e:
            return {"ok": False, "error": "internal", "details": str(e)}

    # Run as stdio server (async API in mcp 2.x)
    await mcp.run_stdio_async()
    return 0


if __name__ == "__main__":
    try:
        rc = asyncio.run(main())
    except KeyboardInterrupt:
        rc = 0
    sys.exit(rc)
