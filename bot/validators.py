"""Validation helpers for CLI order input."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from bot.exceptions import InputValidationError


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


@dataclass(frozen=True)
class OrderRequest:
    symbol: str
    side: str
    order_type: str
    quantity: Decimal
    price: Decimal | None = None


def validate_order_request(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str | None = None,
) -> OrderRequest:
    normalized_symbol = symbol.strip().upper()
    normalized_side = side.strip().upper()
    normalized_order_type = order_type.strip().upper()
    parsed_quantity = parse_positive_decimal(quantity, field_name="quantity")
    parsed_price = (
        parse_positive_decimal(price, field_name="price") if price is not None else None
    )

    if not normalized_symbol:
        raise InputValidationError("Symbol is required.")
    if normalized_side not in VALID_SIDES:
        raise InputValidationError("Side must be BUY or SELL.")
    if normalized_order_type not in VALID_ORDER_TYPES:
        raise InputValidationError("Order type must be MARKET or LIMIT.")
    if normalized_order_type == "LIMIT" and parsed_price is None:
        raise InputValidationError("Price is required for LIMIT orders.")
    if normalized_order_type == "MARKET" and parsed_price is not None:
        raise InputValidationError("Price must not be provided for MARKET orders.")

    return OrderRequest(
        symbol=normalized_symbol,
        side=normalized_side,
        order_type=normalized_order_type,
        quantity=parsed_quantity,
        price=parsed_price,
    )


def parse_positive_decimal(value: str, field_name: str) -> Decimal:
    try:
        decimal_value = Decimal(value)
    except (InvalidOperation, TypeError) as exc:
        raise InputValidationError(
            f"{field_name.capitalize()} must be a valid decimal number."
        ) from exc

    if decimal_value <= 0:
        raise InputValidationError(f"{field_name.capitalize()} must be greater than 0.")

    return decimal_value
