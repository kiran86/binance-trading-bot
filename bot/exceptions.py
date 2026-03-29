"""Application-specific exceptions."""


class TradingBotError(Exception):
    """Base exception for the trading bot."""


class InputValidationError(TradingBotError):
    """Raised when CLI input fails validation."""


class ConfigurationError(TradingBotError):
    """Raised when required configuration is missing."""


class BinanceAPIError(TradingBotError):
    """Raised when Binance returns an API error."""


class NetworkError(TradingBotError):
    """Raised when the application cannot reach Binance."""
