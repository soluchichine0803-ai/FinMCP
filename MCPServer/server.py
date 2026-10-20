
from mcp.server import MCPServer
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

ENV_FILE = Path(__file__).resolve().parent.parent / "logs.env"
load_dotenv(ENV_FILE)

API_URL = os.getenv("FASTBANK_API_URL", "").rstrip("/")
USERNAME = os.getenv("FASTBANK_USERNAME")
PASSWORD = os.getenv("FASTBANK_PASSWORD")

mcp = MCPServer("FastBank")


def api_request(
    method: str,
    endpoint: str,
    json: dict | None = None,
) -> str:
    """Send an authenticated request to the FastBank API."""
    if not API_URL or not USERNAME or not PASSWORD:
        return (
            "Configuration error: check FASTBANK_API_URL, "
            "FASTBANK_USERNAME, and FASTBANK_PASSWORD in logs.env."
        )

    try:
        response = httpx.request(
            method,
            f"{API_URL}/{endpoint.lstrip('/')}",
            auth=(USERNAME, PASSWORD),
            json=json,
            timeout=10.0,
        )

        if response.status_code == 401:
            return "Authentication failed. Check the credentials in logs.env."

        if response.status_code == 403:
            return "Access denied. This account does not have permission to perform this action."

        if response.status_code == 404:
            return "Resource not found, or it is unavailable to this account."

        response.raise_for_status()
        return response.text

    except httpx.TimeoutException:
        return "FastBank API request timed out. Try again."

    except httpx.HTTPStatusError as e:
        return f"FastBank API returned HTTP {e.response.status_code}: {e.response.text}"

    except httpx.RequestError:
        return "Could not connect to FastBank. Check that the Django API is running."

#ping for testing connectivity
@mcp.tool()
def ping() -> str:
    """Check whether the FastBank MCP server is running."""
    return "FastBank MCP is online."


#USER ACCOUNT MANAGEMENT TOOLS
#account tools
@mcp.tool()
def get_my_accounts() -> str:
    """Retrieve the accounts belonging to the currently configured user."""
    return api_request("GET", "/accounts/")

@mcp.tool()
def get_account(account_id: int) -> str:
    """Get details for one of the authenticated user's accounts.
    Use the account's database ID, not its account number.
    """
    return api_request("GET", f"/accounts/{account_id}/")

@mcp.tool()
def update_account(
    account_id: int,
    account_number: str | None = None,
    balance: float | None = None,
    currency: str | None = None,
    status: str | None = None,
) -> str:
    """Update an account's details.
    Provide the account database ID and only the fields to change.
    All update fields are optional, but provide at least one.
    """
    updates = {
        key: value
        for key, value in {
            "account_number": account_number,
            "balance": balance,
            "currency": currency,
            "status": status,
        }.items()
        if value is not None
    }

    if not updates:
        return "No updates provided. Specify at least one field to change."

    return api_request(
        "PATCH",
        f"/accounts/{account_id}/",
        json=updates,
    )

@mcp.tool()
def create_account(
    account_number: str,
    balance: float = 0.0,
    currency: str = "NGN",
    status: str = "active",
) -> str:
    """Create a bank account for the authenticated customer.
    account_number is required. Other fields are optional.
    """
    return api_request(
        "POST",
        "/accounts/create/",
        json={
            "account_number": account_number,
            "balance": balance,
            "currency": currency,
            "status": status,
        },
    )

#transaction tools
@mcp.tool()
def get_my_transactions() -> str:
    """List transactions involving accounts belonging to the authenticated user."""
    return api_request("GET", "/transactions/")


@mcp.tool()
def get_transaction(tid: str) -> str:
    """Retrieve a specific transaction using its UUID, not its integer database ID."""
    return api_request("GET", f"/transactions/{tid}/")


@mcp.tool()
def create_transfer(
    from_account: str,
    to_account: str,
    amount: float,
) -> str:
    """Transfer funds between bank accounts.
    Account arguments are account numbers, not database IDs.
    Only transfer funds from an account owned by the authenticated user.
    """
    return api_request(
        "POST",
        "/transfers/",
        json={
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount,
        },
    )


#ADMINISTRATION TOOLS

@mcp.tool()
def admin_get_users() -> str:
    """ADMIN ONLY: List all registered users for auditing."""
    return api_request("GET", "/adminops/users/")


@mcp.tool()
def admin_get_all_accounts() -> str:
    """ADMIN ONLY: List all bank accounts."""
    return api_request("GET", "/adminops/accounts/")


@mcp.tool()
def admin_get_user(user_id: int) -> str:
    """ADMIN ONLY: View a user's details. Requires the user's database ID."""
    return api_request("GET", f"/adminops/users/{user_id}/")


@mcp.tool()
def admin_get_account(account_id: int) -> str:
    """ADMIN ONLY: View account details. Requires the account's database ID, not its account number."""
    return api_request("GET", f"/adminops/accounts/{account_id}/")


@mcp.tool()
def admin_get_account_transactions(account_id: int) -> str:
    """ADMIN ONLY: List transactions involving an account. Requires the account's database ID."""
    return api_request(
        "GET",
        f"/adminops/accounts/{account_id}/transactions/",
    )


@mcp.tool()
def admin_get_all_transactions() -> str:
    """ADMIN ONLY: List all transactions for auditing."""
    return api_request("GET", "/adminops/transactions/")


@mcp.tool()
def admin_get_transaction(tid: str) -> str:
    """ADMIN ONLY: View a transaction using its UUID TID."""
    return api_request("GET", f"/adminops/transaction/{tid}/")


@mcp.tool()
def admin_get_user_accounts(user_id: int) -> str:
    """ADMIN ONLY: List all accounts belonging to a user. Requires the user's database ID."""
    return api_request(
        "GET",
        f"/adminops/users/{user_id}/accounts/",
    )


@mcp.tool()
def admin_create_customer(
    username: str,
    password: str,
    email: str = "",
) -> str:
    """ADMIN ONLY: Create an ordinary customer user.
    Username and password are required. Email is optional.
    """
    return api_request(
        "POST",
        "/adminops/users/create/",
        json={
            "username": username,
            "password": password,
            "email": email,
        },
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
