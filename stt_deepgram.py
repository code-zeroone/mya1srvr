import asyncio, websockets, ssl, json

class DeepgramSTT:
    def __init__(self, cfg):
        self.q = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self._connect(cfg["deepgram_key"]))

    async def _connect(self, key):
        ssl_ctx = ssl.create_default_context()
        self.ws = await websockets.connect(
            "wss://api.deepgram.com/v1/listen?"
            "encoding=linear16&sample_rate=16000&channels=1",
            headers=[("Authorization", f"Token {key}")],
            ssl=ssl_ctx
        )

        async for msg in self.ws:
            data = json.loads(msg)
            if "channel" in data:
                alt = data["channel"]["alternatives"][0]
                if alt["transcript"]:
                    await self.q.put((alt["transcript"], alt.get("language","auto")))

    async def send_audio(self, data):
        await self.ws.send(data)

    async def get_text(self):
        return await self.q.get()
