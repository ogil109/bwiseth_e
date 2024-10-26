from sqlalchemy import Column, DateTime, Float, Integer, String

from src import Base


class KlineData(Base):
    __tablename__ = "kline_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(10), nullable=False)  # Trading pair (e.g., BTCUSDT)
    interval = Column(String(10), nullable=False)  # Interval (e.g., 1m, 4h, 1d)
    open_price = Column(Float, nullable=False)  # Open price at the start of the interval
    close_price = Column(Float, nullable=False)  # Close price at the end of the interval
    high_price = Column(Float, nullable=False)  # Highest price during the interval
    low_price = Column(Float, nullable=False)  # Lowest price during the interval
    volume = Column(Float, nullable=False)  # Base asset volume
    quote_volume = Column(Float, nullable=False)  # Quote asset volume
    taker_buy_base_vol = Column(Float, nullable=True)  # Taker buy base asset volume
    taker_buy_quote_vol = Column(Float, nullable=True)  # Taker buy quote asset volume
    num_trades = Column(Integer, nullable=False)  # Number of trades
    start_time = Column(DateTime, nullable=False)  # Start time of the Kline interval
    end_time = Column(DateTime, nullable=False)  # End time of the Kline interval (or close)

    def __repr__(self):
        return f"<Kline(symbol={self.symbol}, int={self.interval}, O={self.open_price}, H={self.high_price}, L={self.low_price}, C={self.close_price})>"  # noqa: E501
