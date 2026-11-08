
import asyncio
import sys

from mcp import Client, StdioServerParameters


async def main():
    server = StdioServerParameters(
        command=sys.executable,
        args=["MCPServer/server.py"],
    )

    async with Client(server) as client:
        tools = await client.list_tools()

        # print("Available tools:")
        # for tool in tools.tools:
        #     print(f"- {tool.name}: {tool.description}")

        # print("\nTesting ping...")
        # ping_result = await client.call_tool("ping", {})
        # for item in ping_result.content:
        #     if hasattr(item, "text"):
        #         print(item.text)

        # print("\nTesting get_my_accounts...")
        # accounts_result = await client.call_tool(
        #     "get_my_accounts", {}
        # )

        # for item in accounts_result.content:
        #     if hasattr(item, "text"):
        #         print(item.text)

        
        # print("\nTesting get_account...")
        # result = await client.call_tool("get_account", {"account_id": 1})
        # for item in result.content:
        #     if hasattr(item, "text"):
        #         print(item.text)

        # print("\nTesting get_my_transactions...")
        # result = await client.call_tool("get_my_transactions", {})
        # for item in result.content:
        #     if hasattr(item, "text"):
        #         print(item.text)

        # print("\nTesting get_transaction...")
        # tid = "3797a2b1-7680-4b81-9a9a-813733eb22d8"
        # result = await client.call_tool("get_transaction", {"tid": tid})
        # for item in result.content:
        #     if hasattr(item, "text"):
        #         print(item.text)

        print("\nTesting create_account...")
        result = await client.call_tool(
            "create_account",
            {
                "account_number": "8068069999",
                "balance": 0,
                "currency": "NGN",
                "status": "active",
            },
        )
        for item in result.content:
            if hasattr(item, "text"):
                print(item.text)

if __name__ == "__main__":
    asyncio.run(main())
