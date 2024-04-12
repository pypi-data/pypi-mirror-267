import asyncio
import pytest
import pytest_asyncio

from trinnov_altitude.exceptions import (
    ConnectionFailedError,
    ConnectionTimeoutError,
    InvalidMacAddressOUIError,
    MalformedMacAddressError,
)
from trinnov_altitude.messages import Message
from trinnov_altitude.mocks import MockTrinnovAltitudeServer
from trinnov_altitude.trinnov_altitude import TrinnovAltitude


@pytest_asyncio.fixture
async def mock_server():
    server = MockTrinnovAltitudeServer()
    await server.start_server()
    yield server
    await server.stop_server()


@pytest_asyncio.fixture
async def connected_client():
    client = TrinnovAltitude(host="localhost")
    await client.connect()
    client.start_listening()
    yield client
    await client.stop_listening()
    await client.disconnect()


@pytest.mark.asyncio
async def test_validate_mac():
    with pytest.raises(MalformedMacAddressError):
        TrinnovAltitude.validate_mac("malformed")

    with pytest.raises(InvalidMacAddressOUIError):
        TrinnovAltitude.validate_mac("c9:7f:32:2b:ea:f4")

    assert TrinnovAltitude.validate_mac("c8:7f:54:7a:eb:c2")


@pytest.mark.asyncio
async def test_connect_failed(mock_server):
    client = TrinnovAltitude(host="invalid")
    with pytest.raises(ConnectionFailedError):
        await client.connect()


@pytest.mark.asyncio
async def test_connect_timeout(mock_server):
    client = TrinnovAltitude(host="1.1.1.1")
    with pytest.raises(ConnectionTimeoutError):
        await client.connect(1)


@pytest.mark.asyncio
async def test_connect_success(mock_server):
    client = TrinnovAltitude(host="localhost", port=mock_server.port)
    await client.connect()
    assert client.connected() is True
    await client.disconnect()


@pytest.mark.asyncio
async def test_register_callback(mock_server):
    client = TrinnovAltitude(host="localhost", port=mock_server.port)
    client._last_message = None

    def _update(message: Message):
        client._last_message = message  # type: ignore

    client.register_callback(_update)

    await client.connect()
    client.start_listening()
    await client.wait_for_initial_sync()
    await client.stop_listening()
    await client.disconnect()

    assert client._last_message  # type: ignore


@pytest.mark.asyncio
async def test_start_listening_reconnects(mock_server):
    client = TrinnovAltitude(host="localhost", port=mock_server.port)

    assert not client.connected()
    client.start_listening(reconnect=True)
    await client.wait_for_initial_sync()
    assert client.connected()
    await client.stop_listening()
    await client.disconnect()


# --------------------------
# Commands
# --------------------------


@pytest.mark.asyncio
async def test_volume_adjust(mock_server, connected_client):
    await connected_client.volume_adjust(2)
    await asyncio.sleep(0.5)
    assert connected_client.volume == -38.0


@pytest.mark.asyncio
async def test_volume_set(mock_server, connected_client):
    await connected_client.volume_set(-46)
    await asyncio.sleep(0.5)
    assert connected_client.volume == -46.0
