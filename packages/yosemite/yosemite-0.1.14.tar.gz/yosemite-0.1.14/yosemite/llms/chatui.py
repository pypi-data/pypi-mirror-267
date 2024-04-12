from typing import NoReturn, Union
import base64
import io
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from yosemite.llms.llm import LLM
from yosemite.llms.rag import RAG
from elevenlabs.client import ElevenLabs

class ChatUI:
    def __init__(self, model: Union[LLM, RAG], tts: bool = False, elevenlabs_api_key: str = None):
        self.model = model
        self.tts = tts
        if tts and elevenlabs_api_key:
            self.elevenlabs_client = ElevenLabs(api_key=elevenlabs_api_key)
        else:
            self.elevenlabs_client = None
        self.app = FastAPI()
        self.setup_routes()

    async def get_ai_response(self, message: str):
        if isinstance(self.model, LLM):
            response = self.model.invoke(query=message)
        elif isinstance(self.model, RAG):
            response = self.model.invoke(query=message)
        else:
            raise ValueError("Invalid model type. Expected an instance of LLM or RAG.")
        
        yield {"text": response}

    async def get_audio_response(self, text: str):
        if not self.tts or not self.elevenlabs_client:
            return None

        audio_stream = self.elevenlabs_client.generate(
            text=text,
            voice="Rachel",
            model="eleven_multilingual_v2",
            stream=True
        )

        audio_data = bytearray()
        for chunk in audio_stream:
            audio_data.extend(chunk)

        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        audio_uri = f"data:audio/wav;base64,{audio_base64}"
        return {"audio_uri": audio_uri}

    def setup_routes(self):
        @self.app.get("/")
        async def web_app() -> HTMLResponse:
            with open("yosemite/__resources__/index.html") as f:
                html = f.read()
            return HTMLResponse(html)

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket) -> NoReturn:
            await websocket.accept()
            while True:
                message = await websocket.receive_text()
                async for text_chunk in self.get_ai_response(message):
                    await websocket.send_json(text_chunk)
                    final_text = text_chunk["text"]
                    audio_response = await self.get_audio_response(final_text)
                    if audio_response:
                        await websocket.send_json(audio_response)

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        uvicorn.run(self.app, host=host, port=port, log_level="info")