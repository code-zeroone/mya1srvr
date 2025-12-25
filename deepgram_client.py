import asyncio
import ssl
import json
import websockets

class DeepgramClient:

    def __init__(self):
        self.queue = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self._connect())

    async def _connect(self):
        ssl_ctx = ssl.create_default_context()
        self.ws = await websockets.connect(
            "wss://api.deepgram.com/v1/listen?"
            "encoding=linear16&sample_rate=16000&channels=1&language=ar",
            headers=[("Authorization", "Token YOUR_API_KEY")],
            ssl=ssl_ctx
        )

        async def recv():
            async for msg in self.ws:
                data = json.loads(msg)
                if "channel" in data:
                    txt = data["channel"]["alternatives"][0]["transcript"]
                    if txt:
                        await self.queue.put(txt)

        self.loop.create_task(recv())

    def send_audio(self, data):
        asyncio.run_coroutine_threadsafe(self.ws.send(data), self.loop)

    async def get_text(self):
        return await self.queue.get()
