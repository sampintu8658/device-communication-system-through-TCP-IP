import unittest
from unittest.mock import MagicMock, patch
import asyncio
from main import DeviceConnection, TcpIpProtocol

class TestClient(unittest.TestCase):
    def setUp(self):
        self.device = DeviceConnection('127.0.0.1', 8888, TcpIpProtocol())
        self.device.reader = MagicMock()
        self.device.writer = MagicMock()

    @patch('client.asyncio.open_connection')
    async def test_connect(self, mock_open_connection):
        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_open_connection.return_value = (mock_reader, mock_writer)

        await self.device.connect()
        self.assertEqual(self.device.reader, mock_reader)
        self.assertEqual(self.device.writer, mock_writer)

    async def test_read(self):
        self.device.reader.read.return_value = b'Test Message'
        message = await self.device.read()
        self.assertEqual(message, 'Test Message')

    async def test_write(self):
        await self.device.write('Test Message')
        self.device.writer.write.assert_called_with(b'Test Message')
        self.device.writer.drain.assert_called()

if __name__ == "__main__":
    unittest.main()
