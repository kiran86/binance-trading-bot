# Binance Futures Testnet Trading Bot

Small Python CLI application for placing `MARKET` and `LIMIT` orders on the Binance Futures Testnet (`USDT-M`).

## Features

- Places `BUY` and `SELL` orders against `https://testnet.binancefuture.com`
- Validates CLI input before sending requests
- Separates CLI logic from the Binance API client
- Logs requests, responses, and errors to `logs/trading_bot.log`
- Handles configuration, validation, API, and network errors clearly

## Setup

1. Create and activate a Binance Futures Testnet account.
2. Generate testnet API credentials.
3. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. Export your credentials:

```bash
export BINANCE_API_KEY="your_testnet_key"
export BINANCE_API_SECRET="your_testnet_secret"
```

## Usage

Market order:

```bash
python3 cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

Limit order:

```bash
python3 cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 70000
```

## Output

The CLI prints:

- order request summary
- order response details including `orderId`, `status`, `executedQty`, and `avgPrice`
- a final success or failure message

## Project Structure

```text
bot/
  client.py
  orders.py
  validators.py
  exceptions.py
  logging_config.py
cli.py
tests/test_cli.py
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```
