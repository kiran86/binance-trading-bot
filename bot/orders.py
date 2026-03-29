"""Order placement service layer."""

from __future__ import annotations

import os
from typing import Any

from bot.client import BinanceFuturesTestnetClient
from bot.exceptions import ConfigurationError
from bot.validators import OrderRequest


def load_credentials() -> tuple[str, str]:
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()
    if not api_key or not api_secret:
        raise ConfigurationError(
            "BINANCE_API_KEY and BINANCE_API_SECRET environment variables are required."
        )
    return api_key, api_secret


def submit_order(
    order_request: OrderRequest,
    client: BinanceFuturesTestnetClient | None = None,
) -> dict[str, Any]:
    active_client = client
    if active_client is None:
        api_key, api_secret = load_credentials()
        active_client = BinanceFuturesTestnetClient(
            api_key=api_key,
            api_secret=api_secret,
        )

    return active_client.place_order(
        symbol=order_request.symbol,
        side=order_request.side,
        order_type=order_request.order_type,
        quantity=order_request.quantity,
        price=order_request.price,
    )
