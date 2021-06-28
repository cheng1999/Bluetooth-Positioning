import asyncio, socket
import time

BEACON={}

async def handle_client(reader, writer):
    request = (await reader.read(255)).decode('utf8')
    
    gateway, rssi = str(request).rstrip('\n').split(':')
    BEACON[gateway]=rssi
    writer.close()

async def run_server():
    server = await asyncio.start_server(handle_client, '', 8080)
    async with server:
        await server.serve_forever()


async def positioning_event():
    while True:
        print('async:',BEACON)
        await asyncio.sleep(1)


async def main():
    task1 = asyncio.create_task(positioning_event())
    task2 = asyncio.create_task(run_server())
    await task1
    await task2
asyncio.run(main())

