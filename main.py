import asyncio

class Protocol:
    def read(self, data):
        raise NotImplementedError

    def write(self, message):
        raise NotImplementedError

class TcpIpProtocol(Protocol):
    def read(self, data):
        return data.decode()

    def write(self, message):
        return message.encode()

class DeviceManager:
    def __init__(self):
        self.devices = []

    def add_device(self, ip, port, protocol):
        device = DeviceConnection(ip, port, protocol)
        self.devices.append(device)

    async def connect_devices(self):
        for device in self.devices:
            await device.connect()

    async def communicate_with_devices(self):
        for device in self.devices:
            try:
                if device.reader and device.writer:
                    await device.write('Ping')
                    response = await device.read()
                    print(f"Device response: {response}")
                else:
                    print(f"Device {device.ip}:{device.port} is not connected.")
            except Exception as e:
                print(f"Error communicating with device {device.ip}:{device.port} - {e}")

class DeviceConnection:
    def __init__(self, ip, port, protocol):
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.reader = None
        self.writer = None

    async def connect(self):
        try:
            self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)
            print(f"Connected to {self.ip}:{self.port}")
        except Exception as e:
            print(f"Failed to connect to {self.ip}:{self.port} - {e}")

    async def read(self):
        if not self.reader:
            print("No reader available.")
            return None
        try:
            data = await self.reader.read(100)
            if not data:
                raise ConnectionResetError("Connection lost")
            return self.protocol.read(data)
        except Exception as e:
            print(f"Failed to read from {self.ip}:{self.port} - {e}")
            return None

    async def write(self, message):
        if not self.writer:
            print("No writer available.")
            return
        try:
            self.writer.write(self.protocol.write(message))
            await self.writer.drain()
            print(f"Sent to {self.ip}:{self.port}: {message}")
        except Exception as e:
            print(f"Failed to write to {self.ip}:{self.port} - {e}")

    async def close(self):
        if not self.writer:
            print("No writer available.")
            return
        try:
            self.writer.close()
            await self.writer.wait_closed()
            print(f"Closed connection to {self.ip}:{self.port}")
        except Exception as e:
            print(f"Failed to close connection to {self.ip}:{self.port} - {e}")

async def main():
    manager = DeviceManager()
    manager.add_device('127.0.0.1', 8888, TcpIpProtocol())
    
    await manager.connect_devices()  # Ensure devices are connected

    while True:
        command = input("Enter command (read, write, quit): ").strip().lower()
        if command == 'quit':
            await manager.communicate_with_devices()  # Optionally, communicate before closing
            break
        elif command == 'read':
            await manager.communicate_with_devices()
        elif command == 'write':
            message = input("Enter message to send: ")
            for device in manager.devices:
                await device.write(message)
        else:
            print("Invalid command. Please enter 'read', 'write', or 'quit'.")

if __name__ == "__main__":
    asyncio.run(main())







