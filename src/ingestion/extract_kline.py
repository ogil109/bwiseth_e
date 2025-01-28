import json
import os
from datetime import datetime, timezone
from typing import NoReturn

import websockets

from src.ingestion.kafka_producer import process_kline_data

# WebSocket URL for real-time crypto prices
intervals = os.environ["intervals"].split(",")
symbols = os.environ["symbols"].split(",")

url = base_url = "wss://stream.binance.com:9443/stream?streams="

for symbol in symbols:
    for interval in intervals:
        if url != base_url:
            url = url + f"/{symbol}@kline_{interval}"
        else:
            url = f"{base_url}{symbol}@kline_{interval}"

WS_URL = url


# WebSocket listener function
async def listen() -> NoReturn:
    async with websockets.connect(WS_URL) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)

            # Extract relevant data from the payload
            kline_data = data["data"]["k"]

            kline_data = {
                "symbol": kline_data["s"],
                "interval": kline_data["i"],
                "open": float(kline_data["o"]),
                "close": float(kline_data["c"]),
                "high": float(kline_data["h"]),
                "low": float(kline_data["l"]),
                "vol": float(kline_data["v"]),
                "quote_vol": float(kline_data["q"]),
                "taker_buy_base_vol": float(kline_data["V"]),
                "taker_buy_quote_vol": float(kline_data["Q"]),
                "n_trades": int(kline_data["n"]),
                "start_time": datetime.fromtimestamp(
                    kline_data["t"] / 1000, tz=timezone.utc
                ),
                "end_time": datetime.fromtimestamp(
                    kline_data["T"] / 1000, tz=timezone.utc
                ),
            }

            process_kline_data(kline_data)
