import asyncio, websockets, json
from stt_deepgram import DeepgramSTT
from stt_whisper import WhisperSTT
from translator import Translator

cfg = json.load(open("config.json"))

stt = DeepgramSTT(cfg) if cfg["engine"] == "deepgram" else WhisperSTT(cfg)
translator = Translator(cfg)

async def handler(ws):
    print("Client connected")

    async def recv_audio():
        async for data in ws:
            await stt.send_audio(data)

    async def send_text():
        while True:
            text, lang = await stt.get_text()
            if cfg["translate"]:
                text = translator.translate(text, lang, cfg["target_lang"])
            await ws.send(text)

    await asyncio.gather(recv_audio(), send_text())

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8000):
        print("BAHAA AI Server running on :8000")
        await asyncio.Future()

asyncio.run(main())
