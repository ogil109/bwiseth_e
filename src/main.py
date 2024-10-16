import asyncio
from src.ingestion.extract import listen
from src import init_db

# Entry point for running the script
if __name__ == "__main__":
    # Initialize the database (create tables if necessary)
    init_db()

    # Start listening to the WebSocket
    loop = asyncio.get_event_loop()
    loop.run_until_complete(listen())