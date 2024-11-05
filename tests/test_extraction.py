from datetime import datetime, timezone
from operator import attrgetter
from unittest.mock import MagicMock, patch

import pytest

from src.ingestion.extract_kline import insert_kline
from src.ingestion.models import KlineData


@patch("src.ingestion.extract_kline.get_db_session")
def test_insert_kline(mock_get_db_session):
    # Arrange
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    # Define the input data
    symbol = "btcusdt"
    interval = "1m"
    open_price = 1000
    close_price = 2000
    high_price = 3000
    low_price = 500
    volume = 100
    quote_volume = 200
    taker_buy_base_vol = 10
    taker_buy_quote_vol = 20
    num_trades = 5
    start_time = datetime.now().astimezone(timezone.utc)
    end_time = datetime.now().astimezone(timezone.utc)

    # Act
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

    # Assert that the session was used as a context manager
    mock_get_db_session.return_value.__enter__.assert_called_once()
    mock_get_db_session.return_value.__exit__.assert_called_once()

    # Assert that a KlineData instance was created and added to the session
    mock_session.add.assert_called_once()
    kline_data = mock_session.add.call_args[0][0]
    assert isinstance(kline_data, KlineData)

    attributes = [
        "symbol",
        "interval",
        "open_price",
        "close_price",
        "high_price",
        "low_price",
        "volume",
        "quote_volume",
        "taker_buy_base_vol",
        "taker_buy_quote_vol",
        "num_trades",
        "start_time",
        "end_time",
    ]
    kline_getter = attrgetter(*attributes)
    kline_values = kline_getter(kline_data)
    expected_values = (
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

    for kline_value, expected_value in zip(kline_values, expected_values):
        if isinstance(kline_value, datetime) and isinstance(expected_value, datetime):
            assert abs((kline_value - expected_value).total_seconds()) < 1
        else:
            assert kline_value == expected_value

    # Assert that the session was committed
    mock_session.commit.assert_called_once()


@patch("src.ingestion.extract_kline.get_db_session")
def test_insert_kline_exception(mock_get_db_session):
    # Arrange
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    # Force an exception during add to trigger rollback
    mock_session.add.side_effect = Exception("Insertion error")

    # Act & Assert
    with pytest.raises(Exception, match="Insertion error"):
        insert_kline(
            "btcusdt",
            "1m",
            1000,
            2000,
            3000,
            500,
            100,
            200,
            10,
            20,
            5,
            datetime.now().astimezone(timezone.utc),
            datetime.now().astimezone(timezone.utc),
        )
    mock_session.rollback.assert_called_once()


@patch("src.ingestion.extract_kline.get_db_session")
def test_insert_kline_none_values(mock_get_db_session):
    # Arrange
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    # Define input data with None for optional fields
    symbol = "btcusdt"
    interval = "1m"
    open_price = 1000
    close_price = 2000
    high_price = 3000
    low_price = 500
    volume = None
    quote_volume = None
    taker_buy_base_vol = None
    taker_buy_quote_vol = None
    num_trades = 5
    start_time = datetime.now().astimezone(timezone.utc)
    end_time = datetime.now().astimezone(timezone.utc)

    # Act
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

    # Assert that the session was used as a context manager
    mock_get_db_session.return_value.__enter__.assert_called_once()
    mock_get_db_session.return_value.__exit__.assert_called_once()

    # Assert that a KlineData instance was created and added to the session
    mock_session.add.assert_called_once()
    kline_data = mock_session.add.call_args[0][0]
    assert isinstance(kline_data, KlineData)

    attributes = [
        "symbol",
        "interval",
        "open_price",
        "close_price",
        "high_price",
        "low_price",
        "volume",
        "quote_volume",
        "taker_buy_base_vol",
        "taker_buy_quote_vol",
        "num_trades",
        "start_time",
        "end_time",
    ]
    kline_getter = attrgetter(*attributes)
    kline_values = kline_getter(kline_data)
    expected_values = (
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

    for kline_value, expected_value in zip(kline_values, expected_values):
        if isinstance(kline_value, datetime) and isinstance(expected_value, datetime):
            assert abs((kline_value - expected_value).total_seconds()) < 1
        else:
            assert kline_value == expected_value

    # Assert that the session was committed
    mock_session.commit.assert_called_once()


if __name__ == "__main__":
    pytest.main()
