import asyncio
import openai
import Config

openai.api_key = Config.OPENAI_API


class TTSConventer:
    @staticmethod
    def convert(audio):
        return openai.Audio.transcribe("whisper-1", audio, response_format="text")
