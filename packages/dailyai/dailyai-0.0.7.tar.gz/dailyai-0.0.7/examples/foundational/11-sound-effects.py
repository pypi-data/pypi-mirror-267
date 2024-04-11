import aiohttp
import asyncio
import logging
import os
import wave
from dailyai.pipeline.pipeline import Pipeline

from dailyai.transports.daily_transport import DailyTransport
from dailyai.services.open_ai_services import OpenAILLMService
from dailyai.services.elevenlabs_ai_service import ElevenLabsTTSService
from dailyai.pipeline.aggregators import (
    LLMUserContextAggregator,
    LLMAssistantContextAggregator,
)
from dailyai.services.ai_services import AIService, FrameLogger
from dailyai.pipeline.frames import (
    Frame,
    AudioFrame,
    LLMResponseEndFrame,
    LLMMessagesFrame,
)
from typing import AsyncGenerator

from runner import configure

from dotenv import load_dotenv
load_dotenv(override=True)

logging.basicConfig(format=f"%(levelno)s %(asctime)s %(message)s")
logger = logging.getLogger("dailyai")
logger.setLevel(logging.DEBUG)

sounds = {}
sound_files = ["ding1.wav", "ding2.wav"]

script_dir = os.path.dirname(__file__)

for file in sound_files:
    # Build the full path to the image file
    full_path = os.path.join(script_dir, "assets", file)
    # Get the filename without the extension to use as the dictionary key
    filename = os.path.splitext(os.path.basename(full_path))[0]
    # Open the image and convert it to bytes
    with wave.open(full_path) as audio_file:
        sounds[file] = audio_file.readframes(-1)


class OutboundSoundEffectWrapper(AIService):
    def __init__(self):
        pass

    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        if isinstance(frame, LLMResponseEndFrame):
            yield AudioFrame(sounds["ding1.wav"])
            # In case anything else up the stack needs it
            yield frame
        else:
            yield frame


class InboundSoundEffectWrapper(AIService):
    def __init__(self):
        pass

    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        if isinstance(frame, LLMMessagesFrame):
            yield AudioFrame(sounds["ding2.wav"])
            # In case anything else up the stack needs it
            yield frame
        else:
            yield frame


async def main(room_url: str, token):
    async with aiohttp.ClientSession() as session:
        transport = DailyTransport(
            room_url,
            token,
            "Respond bot",
            duration_minutes=5,
            mic_enabled=True,
            mic_sample_rate=16000,
            camera_enabled=False,
        )
        transport.transcription_settings["extra"]["punctuate"] = True

        llm = OpenAILLMService(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4-turbo-preview")

        tts = ElevenLabsTTSService(
            aiohttp_session=session,
            api_key=os.getenv("ELEVENLABS_API_KEY"),
            voice_id="ErXwobaYiN019PkySvjV",
        )

        messages = [
            {
                "role": "system",
                "content": "You are a helpful LLM in a WebRTC call. Your goal is to demonstrate your capabilities in a succinct way. Your output will be converted to audio. Respond to what the user said in a creative and helpful way.",
            },
        ]

        tma_in = LLMUserContextAggregator(
            messages, transport._my_participant_id)
        tma_out = LLMAssistantContextAggregator(
            messages, transport._my_participant_id
        )
        out_sound = OutboundSoundEffectWrapper()
        in_sound = InboundSoundEffectWrapper()
        fl = FrameLogger("LLM Out")
        fl2 = FrameLogger("Transcription In")

        pipeline = Pipeline([tma_in, in_sound, fl2, llm, tma_out, fl, tts, out_sound])

        @transport.event_handler("on_first_other_participant_joined")
        async def on_first_other_participant_joined(transport, participant):
            await transport.say("Hi, I'm listening!", tts)
            await transport.send_queue.put(AudioFrame(sounds["ding1.wav"]))

        await asyncio.gather(transport.run(pipeline))


if __name__ == "__main__":
    (url, token) = configure()
    asyncio.run(main(url, token))
