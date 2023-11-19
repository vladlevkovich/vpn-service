import asyncio
import ssl
import socket


async def handle_client(reader, writer):
    data = await reader.read(100)
    message = data.decode
    addr = writer.get_extra_info('peername')

    print(f'Received {message} from {addr}')

    print(f'Send: {message}')
    writer.write(data)
    await writer.drain()


