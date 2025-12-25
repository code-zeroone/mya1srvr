import asyncio
import websockets
from deepgram_client import DeepgramClient

dg = DeepgramClient()

async def handler(ws):
    print("Client connected")

    async def recv_audio():
        async for msg in ws:
            dg.send_audio(msg)

    async def send_text():
        while True:
            text = await dg.get_text()
            if text:
                await ws.send(text)

    await asyncio.gather(recv_audio(), send_text())

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8000):
        print("Server started on port 8000")
        await asyncio.Future()

asyncio.run(main())
