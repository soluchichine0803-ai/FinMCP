
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

        print("\nTesting admin_get_users...")
        result = await client.call_tool("admin_get_users", {})
        for item in result.content:
            if hasattr(item, "text"):
                print(item.text)

        print("\nTesting admin_get_all_accounts...")
        result = await client.call_tool("admin_get_all_accounts", {})
        for item in result.content:
            if hasattr(item, "text"):
                print(item.text)

        print("\nTesting admin_get_user...")
        result = await client.call_tool("admin_get_user", {"user_id": 3})
        for item in result.content:
            if hasattr(item, "text"):
                print(item.text)

        print("\nTesting admin_get_account...")
        result = await client.call_tool("admin_get_account", {"account_id": 1})
        for item in result.content:
            if hasattr(item, "text"):
                print(item.text)

        print("\nTesting admin_get_account_transactions...")
        result = await client.call_tool(
            "admin_get_account_transactions",
            {"account_id": 1},
        )
        for item in result.content:
            if hasattr(item, "text"):
                print(item.text)

        print("\nTesting admin_get_all_transactions...")
        result = await client.call_tool("admin_get_all_transactions", {})
        for item in result.content:
            if hasattr(item, "text"):
                print(item.text)

        print("\nTesting admin_get_transaction...")
        result = await client.call_tool(
            "admin_get_transaction",
            {"tid": "3797a2b1-7680-4b81-9a9a-813733eb22d8"},
        )
        for item in result.content:
            if hasattr(item, "text"):
                print(item.text)

        print("\nTesting admin_get_user_accounts...")
        result = await client.call_tool(
            "admin_get_user_accounts",
            {"user_id": 3},
        )
        for item in result.content:
            if hasattr(item, "text"):
                print(item.text)


if __name__ == "__main__":
    asyncio.run(main())
