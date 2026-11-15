from decimal import Decimal

wallets: dict[str, Decimal] = {
    "Alice": Decimal("500.84"),
    "Bob": Decimal("200.19"),
}
transactions: dict[str, list[dict[str, object]]] = {}


def get_balance(wallet_id: str) -> dict[str, object]:
    """Return the USDC balance for a wallet."""
    wallet_id = wallet_id.strip().capitalize()
    if wallet_id not in wallets:
        return {
            "success": False, 
            "code": "WALLET_NOT_FOUND",
            "message": f"Wallet '{wallet_id}' does not exist.",
        }
    return {
        "success": True,
        "wallet": wallet_id,
        "balance": str(wallets[wallet_id]),
    }


def send_payment(from_id: str, to_id: str, amount_usdc: Decimal) -> dict[str, object]:
    """Send a USDC payment from one wallet to another."""

    from_id = from_id.strip().capitalize()
    to_id = to_id.strip().capitalize()
    amount_usdc = Decimal(str(amount_usdc))
    if amount_usdc <= 0:
        return {
            "success": False,
            "code": "INVALID_AMOUNT",
            "message": "Use a positive amount.",
        }
    if from_id not in wallets:
        return {
            "success": False,
            "code": "WALLET_NOT_FOUND",
            "message": f"Sender wallet '{from_id}' does not exist.",
        }
    if to_id not in wallets:
        return {
            "success": False,
            "code": "WALLET_NOT_FOUND",
            "message": f"Recipient wallet '{to_id}' does not exist.",
        }
    if wallets[from_id] < amount_usdc:
        return {
            "success": False,
            "code": "INSUFFICIENT_FUNDS",
            "message": f"Wallet '{from_id}' has insufficient funds.",
        }

    wallets[from_id] -= amount_usdc
    wallets[to_id] += amount_usdc

    transactions.setdefault(from_id, []).append(
        {"type": "sent", "amount": str(amount_usdc), "counterparty": to_id}
    )
    transactions.setdefault(to_id, []).append(
        {"type": "received", "amount": str(amount_usdc), "counterparty": from_id}
    )
    return {
        "success": True,
        "code": "PAYMENT_SENT",
        "message": f"Sent {amount_usdc} USDC from '{from_id}' to '{to_id}'.",
        "details": {
            "from_id_amount": str(wallets[from_id]),
            "to_id_amount": str(wallets[to_id]),
        }
    }


def list_transactions(wallet_id: str) -> list[dict[str, object]] | dict[str, object]:
    """Return the transactions associated with a wallet."""
    wallet_id = wallet_id.strip().capitalize()
    if wallet_id not in wallets:
        return {
            "success": False, 
            "code": "WALLET_NOT_FOUND",
            "message": f"Wallet '{wallet_id}' does not exist.",
        }
    return transactions.get(wallet_id, [])