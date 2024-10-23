import asyncio

from src import init_db
from src.ingestion.extract_kline import listen

# Entry point for running the script
if __name__ == "__main__":
    # Initialize the database (create tables if necessary)
    init_db()

    # Start listening to the WebSocket
    loop = asyncio.get_event_loop()
    loop.run_until_complete(listen())
