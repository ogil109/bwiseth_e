import websockets
import json
from datetime import datetime
from src import get_db_session
from src.ingestion.models import CryptoPrice

# WebSocket URL for real-time crypto prices (BTC/ETH)
WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade/ethusdt@trade"

# Insert data into the database
def insert_into_db(symbol, price, timestamp):
    with get_db_session() as session:
        # use the session here
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
            timestamp = datetime.utcnow()
            
            print(f"Received data: {symbol} - {price} at {timestamp}")
            
            # Insert the price into the database
            insert_into_db(symbol, price, timestamp)
