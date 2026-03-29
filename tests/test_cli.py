import unittest

from cli import parse_order_request
from bot.exceptions import InputValidationError


class ParseOrderRequestTests(unittest.TestCase):
    def test_limit_order_requires_price(self) -> None:
        with self.assertRaises(InputValidationError):
            parse_order_request(
                [
                    "--symbol",
                    "BTCUSDT",
                    "--side",
                    "BUY",
                    "--order-type",
                    "LIMIT",
                    "--quantity",
                    "0.01",
                ]
            )

    def test_market_order_rejects_price(self) -> None:
        with self.assertRaises(InputValidationError):
            parse_order_request(
                [
                    "--symbol",
                    "BTCUSDT",
                    "--side",
                    "BUY",
                    "--order-type",
                    "MARKET",
                    "--quantity",
                    "0.01",
                    "--price",
                    "45000",
                ]
            )

    def test_valid_market_order_parses(self) -> None:
        order_request = parse_order_request(
            [
                "--symbol",
                "btcusdt",
                "--side",
                "sell",
                "--order-type",
                "market",
                "--quantity",
                "0.01",
            ]
        )
        self.assertEqual(order_request.symbol, "BTCUSDT")
        self.assertEqual(order_request.side, "SELL")
        self.assertEqual(order_request.order_type, "MARKET")


if __name__ == "__main__":
    unittest.main()
