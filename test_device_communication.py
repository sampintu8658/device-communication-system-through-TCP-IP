import unittest
from unittest.mock import AsyncMock, patch
import asyncio
from main import DeviceManager, TcpIpProtocol, DeviceConnection

class TestDeviceCommunication(unittest.TestCase):
    def setUp(self):
        self.manager = DeviceManager()
        self.manager.add_device('127.0.0.1', 8888, TcpIpProtocol())

    @patch.object(DeviceConnection, 'connect', new_callable=AsyncMock)
    @patch.object(DeviceConnection, 'write', new_callable=AsyncMock)
    @patch.object(DeviceConnection, 'read', new_callable=AsyncMock)
    async def test_communication(self, mock_read, mock_write, mock_connect):
        # Set up mocks
        mock_connect.return_value = None
        mock_write.return_value = None
        mock_read.return_value = 'Pong'

        await self.manager.connect_devices()  # Ensure devices are connected
        await self.manager.communicate_with_devices()
        
        # Validate interactions
        mock_write.assert_called_with('Ping')
        mock_read.assert_called()
    
    @patch.object(DeviceConnection, 'connect', new_callable=AsyncMock)
    @patch.object(DeviceConnection, 'write', new_callable=AsyncMock)
    @patch.object(DeviceConnection, 'read', new_callable=AsyncMock)
    async def test_connection_lost(self, mock_read, mock_write, mock_connect):
        # Simulate connection loss by having read raise an exception
        mock_connect.return_value = None
        mock_write.return_value = None
        mock_read.side_effect = ConnectionResetError("Connection lost")
        
        await self.manager.connect_devices()  # Ensure devices are connected

        with self.assertRaises(ConnectionResetError):
            await self.manager.communicate_with_devices()

    @patch.object(DeviceConnection, 'connect', new_callable=AsyncMock)
    @patch.object(DeviceConnection, 'write', new_callable=AsyncMock)
    @patch.object(DeviceConnection, 'read', new_callable=AsyncMock)
    async def test_read_all_clients(self, mock_read, mock_write, mock_connect):
        # Set up mocks
        mock_connect.return_value = None
        mock_write.return_value = None
        mock_read.return_value = '127.0.0.1'

        await self.manager.connect_devices()  # Ensure devices are connected
        await self.manager.devices[0].write('read_all')
        response = await self.manager.devices[0].read()
        
        # Validate the response
        self.assertIn('127.0.0.1', response)

if __name__ == "__main__":
    unittest.main()

