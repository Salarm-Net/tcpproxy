import asyncio

async def handle_client(reader, writer, remote_host, remote_port):
    try:
        # Connect to the remote server
        remote_reader, remote_writer = await asyncio.open_connection(remote_host, remote_port)

        async def forward_data(source, destination):
            try:
                while True:
                    data = await source.read(4096)
                    if not data:
                        break
                    destination.write(data)
                    await destination.drain()
            except asyncio.CancelledError:
                pass
            finally:
                destination.close()

        # Start bidirectional data forwarding
        task1 = asyncio.create_task(forward_data(reader, remote_writer))
        task2 = asyncio.create_task(forward_data(remote_reader, writer))

        await asyncio.gather(task1, task2)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        writer.close()

async def start_proxy(local_host, local_port, remote_host, remote_port):
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, remote_host, remote_port),
        local_host,
        local_port
    )
    print(f"Proxy running on {local_host}:{local_port} -> {remote_host}:{remote_port}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    local_host = "127.0.0.1"
    local_port = 8888
    remote_host = "example.com"
    remote_port = 80

    try:
        asyncio.run(start_proxy(local_host, local_port, remote_host, remote_port))
    except KeyboardInterrupt:
        print("Proxy stopped.")