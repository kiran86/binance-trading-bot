"""CLI entry point for placing Binance Futures Testnet orders."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from bot.client import BinanceFuturesTestnetClient
from bot.exceptions import (
    BinanceAPIError,
    ConfigurationError,
    InputValidationError,
    NetworkError,
)
from bot.logging_config import configure_logging
from bot.orders import load_credentials, submit_order
from bot.validators import OrderRequest, validate_order_request


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Place Binance Futures Testnet USDT-M orders."
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument(
        "--order-type",
        required=True,
        dest="order_type",
        help="MARKET or LIMIT",
    )
    parser.add_argument(
        "--quantity",
        required=True,
        help="Order quantity as a positive decimal number",
    )
    parser.add_argument(
        "--price",
        help="Limit price as a positive decimal number; required for LIMIT orders",
    )
    return parser


def parse_order_request(argv: Sequence[str] | None = None) -> OrderRequest:
    args = build_parser().parse_args(argv)
    return validate_order_request(
        symbol=args.symbol,
        side=args.side,
        order_type=args.order_type,
        quantity=args.quantity,
        price=args.price,
    )


def run(argv: Sequence[str] | None = None) -> int:
    logger = configure_logging()

    try:
        order_request = parse_order_request(argv)
        api_key, api_secret = load_credentials()
        client = BinanceFuturesTestnetClient(
            api_key=api_key,
            api_secret=api_secret,
            logger=logger,
        )

        print_order_summary(order_request)
        response = submit_order(order_request, client=client)
        print_order_response(response)
        print("Success: order submitted to Binance Futures Testnet.")
        return 0
    except InputValidationError as exc:
        logger.error("Input validation failed: %s", exc)
        print(f"Failure: {exc}", file=sys.stderr)
        return 2
    except ConfigurationError as exc:
        logger.error("Configuration error: %s", exc)
        print(f"Failure: {exc}", file=sys.stderr)
        return 3
    except NetworkError as exc:
        logger.error("Network error: %s", exc)
        print(f"Failure: {exc}", file=sys.stderr)
        return 4
    except BinanceAPIError as exc:
        logger.error("Binance API error: %s", exc)
        print(f"Failure: {exc}", file=sys.stderr)
        return 5
    except Exception as exc:
        logger.exception("Unexpected error while placing order")
        print(f"Failure: unexpected error: {exc}", file=sys.stderr)
        return 1


def print_order_summary(order_request: OrderRequest) -> None:
    print("Order Request Summary")
    print(f"  Symbol: {order_request.symbol}")
    print(f"  Side: {order_request.side}")
    print(f"  Type: {order_request.order_type}")
    print(f"  Quantity: {order_request.quantity}")
    if order_request.price is not None:
        print(f"  Price: {order_request.price}")


def print_order_response(response: dict[str, object]) -> None:
    avg_price = response.get("avgPrice")
    print("Order Response Details")
    print(f"  orderId: {response.get('orderId', 'N/A')}")
    print(f"  status: {response.get('status', 'N/A')}")
    print(f"  executedQty: {response.get('executedQty', 'N/A')}")
    print(f"  avgPrice: {avg_price if avg_price not in (None, '') else 'N/A'}")


if __name__ == "__main__":
    raise SystemExit(run())
