import json
from datetime import datetime, timezone

import pytest
from pytest_mock import MockerFixture

from src.ingestion.extract_kline import listen


@pytest.mark.asyncio
async def test_listen(mocker: MockerFixture):
    mock_websocket_connect = mocker.patch(
        "websockets.connect", new_callable=mocker.AsyncMock
    )
    mock_websocket = mock_websocket_connect.return_value.__aenter__.return_value
    mock_message = json.dumps(
        {
            "data": {
                "k": {
                    "s": "BTCUSDT",
                    "i": "1m",
                    "o": "50000.0",
                    "c": "51000.0",
                    "h": "52000.0",
                    "l": "49000.0",
                    "v": "100.0",
                    "q": "5000000.0",
                    "V": "50.0",
                    "Q": "2500000.0",
                    "n": 1000,
                    "t": 1620000000000,
                    "T": 1620000060000,
                }
            }
        }
    )
    mock_websocket.recv = mocker.AsyncMock(return_value=mock_message)

    mock_process_kline_data = mocker.patch(
        "src.ingestion.kafka_producer.process_kline_data"
    )
    await listen()
    mock_process_kline_data.assert_called_once_with(
        {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "open": 50000.0,
            "close": 51000.0,
            "high": 52000.0,
            "low": 49000.0,
            "vol": 100.0,
            "quote_vol": 5000000.0,
            "taker_buy_base_vol": 50.0,
            "taker_buy_quote_vol": 2500000.0,
            "n_trades": 1000,
            "start_time": datetime.fromtimestamp(1620000000, tz=timezone.utc),
            "end_time": datetime.fromtimestamp(1620000060, tz=timezone.utc),
        }
    )
