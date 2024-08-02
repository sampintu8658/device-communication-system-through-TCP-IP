import asyncio

clients = []

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    clients.append((reader, writer))
    print(f"Accepted connection from {addr}")

    try:
        while True:
            data = await reader.read(100)
            if not data:
                print(f"Connection lost from {addr}")
                break

            message = data.decode()
            print(f"Received {message} from {addr}")

            if message == 'read_all':
                response = '\n'.join([f"{r.get_extra_info('peername')}: {await r.read(100).decode()}" for r, w in clients if w != writer])
                writer.write(response.encode())
                await writer.drain()
            else:
                # Broadcast message to all other clients
                for r, w in clients:
                    if w != writer:
                        w.write(data)
                        await w.drain()
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        print(f"Closing connection to {addr}")
        writer.close()
        await writer.wait_closed()
        clients.remove((reader, writer))

async def run_server():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    async with server:
        print("Server started on 127.0.0.1:8888")
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(run_server())







