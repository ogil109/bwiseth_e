from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, timezone
from src import Base

# Define the CryptoPrice model (maps to the 'crypto_prices' table)
class CryptoPrice(Base):
    __tablename__ = 'crypto_prices'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<CryptoPrice(symbol={self.symbol}, price={self.price}, timestamp={self.timestamp})>"
