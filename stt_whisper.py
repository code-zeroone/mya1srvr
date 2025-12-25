import asyncio, whisper, numpy as np

class WhisperSTT:
    def __init__(self, cfg):
        self.model = whisper.load_model(cfg["whisper_model"])
        self.q = asyncio.Queue()
        self.buffer = b""

    async def send_audio(self, data):
        self.buffer += data
        if len(self.buffer) > 32000:
            audio = np.frombuffer(self.buffer, np.int16).astype("float32") / 32768.0
            self.buffer = b""
            result = self.model.transcribe(audio)
            await self.q.put((result["text"], result["language"]))

    async def get_text(self):
        return await self.q.get()
