import websockets
import json
from datetime import datetime
from src import get_db_session
from src.ingestion.models import KlineData

# WebSocket URL for real-time crypto prices (BTC/ETH)
WS_URL = "wss://stream.binance.com:9443/stream?streams=btcusdt@kline_1m/ethusdt@kline_1m/btcusdt@kline_15m/ethusdt@kline_15m/btcusdt@kline_4h/ethusdt@kline_4h/btcusdt@kline_1d/ethusdt@kline_1d/btcusdt@kline_1w/ethusdt@kline_1w"

def insert_kline(symbol, interval, open_price, close_price, high_price, low_price, volume, quote_volume, taker_buy_base_vol, taker_buy_quote_vol, num_trades, start_time, end_time):
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
            end_time=end_time
        )
        session.add(kline_data)
        session.commit()

# WebSocket listener function
async def listen():
    async with websockets.connect(WS_URL) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            
            # Extract relevant data from the payload
            kline_data = data['data']['k']
            
            symbol = kline_data['s']
            interval = kline_data['i']
            open_price = float(kline_data['o'])
            close_price = float(kline_data['c'])
            high_price = float(kline_data['h'])
            low_price = float(kline_data['l'])
            volume = float(kline_data['v'])
            quote_volume = float(kline_data['q'])
            taker_buy_base_vol = float(kline_data['V'])
            taker_buy_quote_vol = float(kline_data['Q'])
            num_trades = int(kline_data['n'])
            
            start_time = datetime.fromtimestamp(kline_data['t'] / 1000, tz=datetime.timezone.utc)  # Kline start time
            end_time = datetime.fromtimestamp(kline_data['T'] / 1000, tz=datetime.timezone.utc)    # Kline close time

            # Insert the price into the database
            insert_kline(
                symbol, interval, open_price, close_price, high_price, low_price,
                volume, quote_volume, taker_buy_base_vol, taker_buy_quote_vol,
                num_trades, start_time, end_time
            )