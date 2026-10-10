import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "app.mcp.server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            print("\nAVAILABLE MCP TOOLS")
            print("=" * 50)

            tools = await session.list_tools()

            for tool in tools.tools:
                print(f"- {tool.name}")

            print("\nCALLING PRODUCT SEARCH")
            print("=" * 50)

            result = await session.call_tool(
                "product_search",
                {
                    "query": "wireless headphones with long battery life"
                },
            )

            for content in result.content:
                if hasattr(content, "text"):
                    print(content.text)


if __name__ == "__main__":
    asyncio.run(main())