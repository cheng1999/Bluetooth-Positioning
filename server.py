
import asyncio, socket
import time

BEACON={}

async def handle_client(reader, writer):
    global BEACON
    while True:
        request = (await reader.read(255)).decode('utf8')

        if not request: break

        gateway, rssi = str(request).rstrip('\n').split(':')
        BEACON[gateway]=rssi
        await writer.drain()
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

