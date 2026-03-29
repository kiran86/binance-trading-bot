"""Binance Futures Testnet REST client."""

from __future__ import annotations

import hashlib
import hmac
import logging
import time
from decimal import Decimal
from typing import Any
from urllib.parse import urlencode

import requests

from bot.exceptions import BinanceAPIError, NetworkError


class BinanceFuturesTestnetClient:
    """Minimal client for Binance Futures Testnet USDT-M orders."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://testnet.binancefuture.com",
        timeout: int = 10,
        logger: logging.Logger | None = None,
    ) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.logger = logger or logging.getLogger("trading_bot")
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: Decimal,
        price: Decimal | None = None,
    ) -> dict[str, Any]:
        """Place a MARKET or LIMIT order."""
        params: dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": self._format_decimal(quantity),
            "timestamp": int(time.time() * 1000),
            "recvWindow": 5000,
        }
        if price is not None:
            params["price"] = self._format_decimal(price)
            params["timeInForce"] = "GTC"

        signed_payload = self._sign_params(params)
        url = f"{self.base_url}/fapi/v1/order"

        self.logger.info(
            "Submitting Binance order request | url=%s | params=%s",
            url,
            self._safe_log_params(params),
        )

        try:
            response = self.session.post(url, params=signed_payload, timeout=self.timeout)
        except requests.RequestException as exc:
            self.logger.exception("Network failure during Binance order request")
            raise NetworkError(f"Failed to reach Binance testnet: {exc}") from exc

        self.logger.info(
            "Received Binance order response | status_code=%s | body=%s",
            response.status_code,
            response.text,
        )

        try:
            payload = response.json()
        except ValueError as exc:
            self.logger.exception("Binance returned a non-JSON response")
            raise BinanceAPIError(
                f"Binance returned an invalid response: {response.text}"
            ) from exc

        if response.status_code >= 400:
            message = payload.get("msg", "Unknown Binance API error")
            code = payload.get("code", "N/A")
            raise BinanceAPIError(f"Binance API error {code}: {message}")

        return payload

    def _sign_params(self, params: dict[str, Any]) -> dict[str, Any]:
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        signed = dict(params)
        signed["signature"] = signature
        return signed

    @staticmethod
    def _format_decimal(value: Decimal) -> str:
        return format(value.normalize(), "f")

    @staticmethod
    def _safe_log_params(params: dict[str, Any]) -> dict[str, Any]:
        return {key: value for key, value in params.items() if key != "signature"}
