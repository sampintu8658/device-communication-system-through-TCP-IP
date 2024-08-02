import unittest
from unittest.mock import MagicMock, patch
import asyncio
from run_server import handle_client, clients

class TestServer(unittest.TestCase):
    def setUp(self):
        # Clear the clients list before each test
        clients.clear()

    @patch('run_server.asyncio.open_connection')
    async def test_handle_client(self, mock_open_connection):
        # Set up mock reader and writer
        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_open_connection.return_value = (mock_reader, mock_writer)

        # Mock client address and data
        mock_writer.get_extra_info.return_value = ('127.0.0.1', 8888)
        mock_reader.read.return_value = b'Hello World'

        # Simulate the handle_client coroutine
        await handle_client(mock_reader, mock_writer)

        # Check if client is added
        self.assertIn((mock_reader, mock_writer), clients)
        mock_writer.write.assert_called_with(b'Hello World')
        mock_writer.drain.assert_called()

    @patch('run_server.asyncio.start_server')
    async def test_run_server(self, mock_start_server):
        # Mock server start
        mock_server = MagicMock()
        mock_start_server.return_value = mock_server

        # Simulate server running
        await mock_server.serve_forever()

        mock_start_server.assert_called_with(handle_client, '127.0.0.1', 8888)

if __name__ == "__main__":
    unittest.main()


