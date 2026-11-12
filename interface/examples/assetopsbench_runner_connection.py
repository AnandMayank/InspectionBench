#!/usr/bin/env python3
"""Illustration (Appendix K.4): running an AssetOpsBench agent harness against the InspectionBench MCP servers.

NOT used for any reported score. The reported scores come from the in-process two-call reference harness (Appendix K.2).

The InspectionBench robot server is a FastMCP server registered next to the AssetOpsBench servers in
`src/agent/runner.py::DEFAULT_SERVER_PATHS` ("robot": "robot-mcp-server", entry point `servers.robot.main:main` in
pyproject.toml). Every AssetOpsBench runner (PlanExecuteRunner, ClaudeAgentRunner, OpenAIAgentRunner, DeepAgentRunner,
StirrupAgentRunner) launches each server as a stdio MCP process and receives the tools' JSON schemas from FastMCP.
That is the "full-schema" interface, as opposed to the names-only reference harness.

Default (no flag): prints the server map this script would use; no process is launched and no model is called.
With --list-tools: launches the MCP servers over stdio and lists the advertised tools (no model call).
With --execute "<question>": runs one AssetOpsBench runner (requires that runner's model credentials; makes model calls).

Run from the AssetOpsBench root, e.g.:
  uv run python rebuttal_evidence/staged_v4/stage6_evidence_utilization/interface_rebuttal_v1/examples/assetopsbench_runner_connection.py --list-tools
  uv run plan-execute "Inspect chiller_6: read its gauge and decide COMMIT, ESCALATE or ABORT."   # equivalent CLI path
"""
import argparse
import json
import sys

sys.path.insert(0, "src")

INSPECTION_SERVERS = {  # subset of agent.runner.DEFAULT_SERVER_PATHS used by inspection episodes
    "robot": "robot-mcp-server",   # read_gauge, capture_image, navigate_to, safety_gate_check, ... (29 tools)
    "wo": "wo-mcp-server",         # work-order records (14 tools)
    "iot": "iot-mcp-server",       # telemetry (4 tools)
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-tools", action="store_true")
    ap.add_argument("--execute", metavar="QUESTION")
    ap.add_argument("--runner", default="openai", choices=["openai", "claude", "deep"])  # plan-execute: use the `uv run plan-execute` CLI
    ap.add_argument("--model", default=None, help="model id understood by the chosen runner (defaults to the runner's own default)")
    a = ap.parse_args()
    from agent.runner import DEFAULT_SERVER_PATHS
    assert all(DEFAULT_SERVER_PATHS[k] == v for k, v in INSPECTION_SERVERS.items()), "registry changed"
    print(json.dumps({"server_paths": INSPECTION_SERVERS, "registered_in": "src/agent/runner.py::DEFAULT_SERVER_PATHS"}, indent=1))
    if a.list_tools:
        import anyio
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        async def _list():
            for name, entry in INSPECTION_SERVERS.items():
                async with stdio_client(StdioServerParameters(command="uv", args=["run", entry])) as (r, w):
                    async with ClientSession(r, w) as s:
                        await s.initialize()
                        tools = (await s.list_tools()).tools
                        print(name, len(tools), [t.name for t in tools][:8], "...")
        anyio.run(_list)
    if a.execute:
        import anyio
        if a.runner == "openai":
            from agent.openai_agent import OpenAIAgentRunner as Runner
        elif a.runner == "claude":
            from agent.claude_agent.runner import ClaudeAgentRunner as Runner
        else:
            from agent.deep_agent.runner import DeepAgentRunner as Runner
        print("NOTE: this makes model calls and is outside the reported evaluation.", file=sys.stderr)
        kw = {"server_paths": INSPECTION_SERVERS}
        if a.model:
            kw["model"] = a.model
        runner = Runner(**kw)  # multi-turn tool-calling agent (OpenAI/Claude: max_turns=30; Deep agent: recursion_limit=100)
        res = anyio.run(runner.run, a.execute)
        print(getattr(res, "answer", res))


if __name__ == "__main__":
    main()
