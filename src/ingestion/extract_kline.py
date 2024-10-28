import json
from datetime import datetime, timezone
from typing import NoReturn

import websockets

from src.ingestion.models import KlineData
from src.utils.database import get_db_session

# WebSocket URL for real-time crypto prices
with open("/app/config.json") as f:
    config = json.load(f)

intervals = config["market_data"]["intervals"]
symbols = config["market_data"]["symbols"]

url = base_url = "wss://stream.binance.com:9443/stream?streams="

for symbol in symbols:
    for interval in intervals:
        if url != base_url:
            url = url + f"/{symbol}@kline_{interval}"
        else:
            url = f"{base_url}{symbol}@kline_{interval}"

WS_URL = url


def insert_kline(
    symbol,
    interval,
    open_price,
    close_price,
    high_price,
    low_price,
    volume,
    quote_volume,
    taker_buy_base_vol,
    taker_buy_quote_vol,
    num_trades,
    start_time,
    end_time,
) -> None:  # noqa: E501
    with get_db_session() as session:
        kline_data = KlineData(
            symbol=symbol,
            interval=interval,
            open_price=open_price,
            close_price=close_price,
            high_price=high_price,
            low_price=low_price,
            volume=volume,
            quote_volume=quote_volume,
            taker_buy_base_vol=taker_buy_base_vol,
            taker_buy_quote_vol=taker_buy_quote_vol,
            num_trades=num_trades,
            start_time=start_time,
            end_time=end_time,
        )
        session.add(kline_data)
        session.commit()


# WebSocket listener function
async def listen() -> NoReturn:
    async with websockets.connect(WS_URL) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)

            # Extract relevant data from the payload
            kline_data = data["data"]["k"]

            symbol = kline_data["s"]
            interval = kline_data["i"]
            open_price = float(kline_data["o"])
            close_price = float(kline_data["c"])
            high_price = float(kline_data["h"])
            low_price = float(kline_data["l"])
            volume = float(kline_data["v"])
            quote_volume = float(kline_data["q"])
            taker_buy_base_vol = float(kline_data["V"])
            taker_buy_quote_vol = float(kline_data["Q"])
            num_trades = int(kline_data["n"])

            start_time = datetime.fromtimestamp(kline_data["t"] / 1000, tz=timezone.utc)
            end_time = datetime.fromtimestamp(kline_data["T"] / 1000, tz=timezone.utc)

            # Insert the price into the database
            insert_kline(
                symbol,
                interval,
                open_price,
                close_price,
                high_price,
                low_price,
                volume,
                quote_volume,
                taker_buy_base_vol,
                taker_buy_quote_vol,
                num_trades,
                start_time,
                end_time,
            )
