import json

from pytest_mock import MockerFixture

from src.ingestion.kafka_producer import process_kline_data, send_to_kafka


def test_send_to_kafka(mocker: MockerFixture):
    mock_producer = mocker.patch("src.ingestion.kafka_producer.producer")
    mock_producer.produce = mocker.MagicMock()
    mock_producer.flush = mocker.MagicMock()

    data = {"key": "value"}
    send_to_kafka("test_topic", data)

    mock_producer.produce.assert_called_once_with(
        "test_topic",
        key=None,
        value=json.dumps(data),
        callback=mock_producer.delivery_report,
    )
    mock_producer.flush.assert_called_once()


def test_process_kline_data(mocker: MockerFixture):
    mock_send_to_kafka = mocker.patch("src.ingestion.kafka_producer.send_to_kafka")
    kline_data = {"symbol": "BTCUSDT"}
    process_kline_data(kline_data)
    mock_send_to_kafka.assert_called_once_with("kline_topic", kline_data)
