
import asyncio, socket

x=[]

async def handle_client(reader, writer):
    request = 1 
    while request:
        request = (await reader.read(255)).decode('utf8')
        x.append(str(request))
        response = str(request)
        await writer.drain()
    writer.close()

async def run_server():
    server = await asyncio.start_server(handle_client, '', 8080)
    async with server:
        await server.serve_forever()

asyncio.run(run_server())
