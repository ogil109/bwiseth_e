import websockets
import json
from datetime import datetime, timezone
from src import get_db_session
from src.ingestion.models import CryptoPrice

# WebSocket URL for real-time crypto prices (BTC/ETH)
WS_URL = "wss://stream.binance.com:9443/stream?streams=btcusdt@aggTrade/ethusdt@aggTrade"

# Insert data into the database
def insert_into_db(symbol, price, timestamp):
    with get_db_session() as session:
        crypto_price = CryptoPrice(symbol=symbol, price=price, timestamp=timestamp)
        session.add(crypto_price)
        session.commit()

# WebSocket listener function
async def listen():
    async with websockets.connect(WS_URL) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            
            symbol = data['s']
            price = float(data['p'])
            timestamp = datetime.now(timezone.utc)
            
            print(f"Received data: {symbol} - {price} at {timestamp}")
            
            # Insert the price into the database
            insert_into_db(symbol, price, timestamp)
