import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPToolClient:
    def __init__(self):
        self.server_params = StdioServerParameters(
            command="python",
            args=["-m", "app.mcp.server"],
        )

    async def call_tools(self, tools: list[tuple[str, dict]]) -> list[str]:
        results = []

        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:

                await session.initialize()

                for tool_name, arguments in tools:
                    result = await session.call_tool(
                        tool_name,
                        arguments,
                    )

                    output = []

                    for content in result.content:
                        if hasattr(content, "text"):
                            output.append(content.text)

                    results.append("\n".join(output))

        return results

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict,
    ) -> str:
        results = await self.call_tools([
            (tool_name, arguments)
        ])

        return results[0]


def call_mcp_tool(tool_name: str, arguments: dict) -> str:
    return asyncio.run(
        MCPToolClient().call_tool(
            tool_name,
            arguments,
        )
    )


def call_mcp_tools(tools: list[tuple[str, dict]]) -> list[str]:
    return asyncio.run(
        MCPToolClient().call_tools(tools)
    )