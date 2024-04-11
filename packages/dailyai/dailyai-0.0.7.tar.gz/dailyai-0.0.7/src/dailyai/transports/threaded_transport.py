from abc import abstractmethod
import asyncio
import itertools
import numpy as np

import queue
import threading
import time
from typing import Any, AsyncGenerator
from enum import Enum
from dailyai.pipeline.frame_processor import FrameProcessor

from dailyai.pipeline.frames import (
    SendAppMessageFrame,
    AudioFrame,
    EndFrame,
    ImageFrame,
    Frame,
    PipelineStartedFrame,
    SpriteFrame,
    StartFrame,
    TextFrame,
    UserImageRequestFrame,
    UserStartedSpeakingFrame,
    UserStoppedSpeakingFrame,
)
from dailyai.pipeline.pipeline import Pipeline
from dailyai.services.ai_services import TTSService
from dailyai.transports.abstract_transport import AbstractTransport


# Provided by Alexander Veysov


def int2float(sound):
    try:
        abs_max = np.abs(sound).max()
        sound = sound.astype("float32")
        if abs_max > 0:
            sound *= 1 / 32768
        sound = sound.squeeze()  # depends on the use case
        return sound
    except ValueError:
        return sound


class VADState(Enum):
    QUIET = 1
    STARTING = 2
    SPEAKING = 3
    STOPPING = 4


class ThreadedTransport(AbstractTransport):

    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._vad_start_s = kwargs.get("vad_start_s") or 0.2
        self._vad_stop_s = kwargs.get("vad_stop_s") or 0.8
        self._context = kwargs.get("context") or []
        self._vad_enabled = kwargs.get("vad_enabled") or False
        self._has_webrtc_vad = kwargs.get("has_webrtc_vad") or False
        if self._vad_enabled and self._speaker_enabled:
            raise Exception(
                "Sorry, you can't use speaker_enabled and vad_enabled at the same time. Please set one to False."
            )
        self._vad_samples = 1536

        if self._vad_enabled:
            try:
                global torch, torchaudio
                import torch
                # We don't use torchaudio here, but we need to try importing it because
                # Silero uses it
                import torchaudio
                torch.set_num_threads(1)

                (self.model, self.utils) = torch.hub.load(
                    repo_or_dir="snakers4/silero-vad", model="silero_vad", force_reload=False
                )
                self._logger.debug("Loaded Silero VAD")

            except ModuleNotFoundError as e:
                if self._has_webrtc_vad:
                    self._logger.debug(
                        f"Couldn't load torch; using webrtc VAD")
                    self._vad_samples = int(self._speaker_sample_rate / 100.0)
                else:
                    self._logger.error(f"Exception: {e}")
                    self._logger.error(
                        "In order to use Silero VAD, you'll need to `pip install dailyai[silero].")
                    raise Exception(f"Missing module(s): {e}")

        vad_frame_s = self._vad_samples / self._speaker_sample_rate
        self._vad_start_frames = round(self._vad_start_s / vad_frame_s)
        self._vad_stop_frames = round(self._vad_stop_s / vad_frame_s)
        self._vad_starting_count = 0
        self._vad_stopping_count = 0
        self._vad_state = VADState.QUIET
        self._user_is_speaking = False

        self._threadsafe_send_queue = queue.Queue()

        self._images = None

        try:
            self._loop: asyncio.AbstractEventLoop | None = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = None

        self._stop_threads = threading.Event()
        self._is_interrupted = threading.Event()

    async def run(self, pipeline: Pipeline | None = None, override_pipeline_source_queue=True):
        self._prerun()

        async_output_queue_marshal_task = asyncio.create_task(
            self._marshal_frames())

        self._camera_thread = threading.Thread(
            target=self._run_camera, daemon=True)
        self._camera_thread.start()

        self._frame_consumer_thread = threading.Thread(
            target=self._frame_consumer, daemon=True
        )
        self._frame_consumer_thread.start()

        if self._speaker_enabled:
            self._receive_audio_thread = threading.Thread(
                target=self._receive_audio, daemon=True
            )
            self._receive_audio_thread.start()

        if self._vad_enabled:
            self._vad_thread = threading.Thread(target=self._vad, daemon=True)
            self._vad_thread.start()

        pipeline_task = None
        if pipeline:
            pipeline_task = asyncio.create_task(
                self.run_pipeline(pipeline, override_pipeline_source_queue)
            )

        try:
            while time.time() < self._expiration and not self._stop_threads.is_set():
                await asyncio.sleep(1)
        except Exception as e:
            self._logger.error(f"Exception {e}")
            raise e
        finally:
            # Do anything that must be done to clean up
            self._post_run()

        self._stop_threads.set()

        if pipeline_task:
            pipeline_task.cancel()

        await self.send_queue.put(EndFrame())

        await async_output_queue_marshal_task
        self._frame_consumer_thread.join()

        if self._speaker_enabled:
            self._receive_audio_thread.join()

        if self._vad_enabled:
            self._vad_thread.join()

    async def run_pipeline(self, pipeline: Pipeline, override_pipeline_source_queue=True):
        pipeline.set_sink(self.send_queue)
        if override_pipeline_source_queue:
            pipeline.set_source(self.receive_queue)
        await pipeline.run_pipeline()

    async def run_interruptible_pipeline(
        self,
        pipeline: Pipeline,
        pre_processor: FrameProcessor | None = None,
        post_processor: FrameProcessor | None = None,
    ):
        pipeline.set_sink(self.send_queue)
        source_queue = asyncio.Queue()
        pipeline.set_source(source_queue)
        pipeline_task = asyncio.create_task(pipeline.run_pipeline())

        async def yield_frame(frame: Frame) -> AsyncGenerator[Frame, None]:
            yield frame

        async def post_process(post_processor: FrameProcessor):
            while True:
                frame = await self.completed_queue.get()

                # We ignore the output of the post_processor's process frame;
                # this is called to update the post-processor's state.
                async for frame in post_processor.process_frame(frame):
                    pass

                if isinstance(frame, EndFrame):
                    break

        if post_processor:
            post_process_task = asyncio.create_task(
                post_process(post_processor))

        started = False

        async for frame in self.get_receive_frames():
            if isinstance(frame, UserStartedSpeakingFrame):
                pipeline_task.cancel()
                self.interrupt()
                pipeline_task = asyncio.create_task(pipeline.run_pipeline())
                started = False

            if not started:
                await self.send_queue.put(StartFrame())

            if pre_processor:
                frame_generator = pre_processor.process_frame(frame)
            else:
                frame_generator = yield_frame(frame)

            async for frame in frame_generator:
                await source_queue.put(frame)

            if isinstance(frame, EndFrame):
                break

        await asyncio.gather(pipeline_task, post_process_task)

    async def say(self, text: str, tts: TTSService):
        """Say a phrase. Use with caution; this bypasses any running pipelines."""
        async for frame in tts.process_frame(TextFrame(text)):
            await self.send_queue.put(frame)

    def _post_run(self):
        # Note that this function must be idempotent! It can be called multiple times
        # if, for example, a keyboard interrupt occurs.
        pass

    def stop(self):
        self._stop_threads.set()

    async def stop_when_done(self):
        await self._wait_for_send_queue_to_empty()
        self.stop()

    async def _wait_for_send_queue_to_empty(self):
        await self.send_queue.join()
        self._threadsafe_send_queue.join()

    @abstractmethod
    def write_frame_to_camera(self, frame: bytes):
        pass

    @abstractmethod
    def write_frame_to_mic(self, frame: bytes):
        pass

    @abstractmethod
    def read_audio_frames(self, desired_frame_count):
        return bytes()

    @abstractmethod
    def _prerun(self):
        pass

    def _silero_vad_analyze(self):
        try:
            audio_chunk = self.read_audio_frames(self._vad_samples)
            audio_int16 = np.frombuffer(audio_chunk, np.int16)
            audio_float32 = int2float(audio_int16)
            new_confidence = self.model(
                torch.from_numpy(audio_float32), 16000).item()
            # yeses = int(new_confidence * 20.0)
            # nos = 20 - yeses
            # out = "!" * yeses + "." * nos
            # print(f"!!! confidence: {out}")
            speaking = new_confidence > 0.5
            return speaking
        except BaseException:
            # This comes from an empty audio array
            return False

    def _vad(self):

        while not self._stop_threads.is_set():
            if hasattr(self, 'model'):  # we can use Silero
                speaking = self._silero_vad_analyze()
            elif self._has_webrtc_vad:
                speaking = self._webrtc_vad_analyze()
            else:
                raise Exception("VAD is running with no VAD service available")
            if speaking:
                match self._vad_state:
                    case VADState.QUIET:
                        self._vad_state = VADState.STARTING
                        self._vad_starting_count = 1
                    case VADState.STARTING:
                        self._vad_starting_count += 1
                    case VADState.STOPPING:
                        self._vad_state = VADState.SPEAKING
                        self._vad_stopping_count = 0
            else:
                match self._vad_state:
                    case VADState.STARTING:
                        self._vad_state = VADState.QUIET
                        self._vad_starting_count = 0
                    case VADState.SPEAKING:
                        self._vad_state = VADState.STOPPING
                        self._vad_stopping_count = 1
                    case VADState.STOPPING:
                        self._vad_stopping_count += 1

            if (
                self._vad_state == VADState.STARTING
                and self._vad_starting_count >= self._vad_start_frames
            ):
                if self._loop:
                    asyncio.run_coroutine_threadsafe(
                        self.receive_queue.put(
                            UserStartedSpeakingFrame()), self._loop)
                # self.interrupt()
                self._vad_state = VADState.SPEAKING
                self._vad_starting_count = 0
            if (
                self._vad_state == VADState.STOPPING
                and self._vad_stopping_count >= self._vad_stop_frames
            ):

                if self._loop:
                    asyncio.run_coroutine_threadsafe(
                        self.receive_queue.put(
                            UserStoppedSpeakingFrame()), self._loop)
                self._vad_state = VADState.QUIET
                self._vad_stopping_count = 0

    async def _marshal_frames(self):
        while True:
            frame: Frame | list = await self.send_queue.get()
            self._threadsafe_send_queue.put(frame)
            self.send_queue.task_done()
            if isinstance(frame, EndFrame):
                break

    def interrupt(self):
        self._logger.debug("### Interrupting")
        self._is_interrupted.set()

    async def get_receive_frames(self) -> AsyncGenerator[Frame, None]:
        while True:
            frame = await self.receive_queue.get()
            yield frame
            if isinstance(frame, EndFrame):
                break

    def _receive_audio(self):
        if not self._loop:
            self._logger.error("No loop available for audio thread")
            return

        seconds = 1
        desired_frame_count = self._speaker_sample_rate * seconds
        while not self._stop_threads.is_set():
            buffer = self.read_audio_frames(desired_frame_count)
            if len(buffer) > 0:
                frame = AudioFrame(buffer)
                asyncio.run_coroutine_threadsafe(
                    self.receive_queue.put(frame), self._loop
                )

        asyncio.run_coroutine_threadsafe(
            self.receive_queue.put(
                EndFrame()), self._loop)

    def _set_image(self, image: bytes):
        self._images = itertools.cycle([image])

    def _set_images(self, images: list[bytes], start_frame=0):
        self._images = itertools.cycle(images)

    def request_participant_image(self, participant_id: str):
        """ Child classes should override this to force an image from a user. """
        pass

    def send_app_message(self, message: Any, participant_id: str | None):
        """ Child classes should override this to send a custom message to the room. """
        pass

    def _run_camera(self):
        try:
            while not self._stop_threads.is_set():
                if self._images:
                    this_frame = next(self._images)
                    self.write_frame_to_camera(this_frame)

                time.sleep(1.0 / self._camera_framerate)
        except Exception as e:
            self._logger.error(f"Exception {e} in camera thread.")
            raise e

    def _frame_consumer(self):
        self._logger.info("🎬 Starting frame consumer thread")
        b = bytearray()
        smallest_write_size = 3200
        largest_write_size = 8000
        while True:
            try:
                frames_or_frame: Frame | list[Frame] = self._threadsafe_send_queue.get(
                )
                if (
                    isinstance(frames_or_frame, AudioFrame)
                    and len(frames_or_frame.data) > largest_write_size
                ):
                    # subdivide large audio frames to enable interruption
                    frames = []
                    for i in range(0, len(frames_or_frame.data),
                                   largest_write_size):
                        frames.append(AudioFrame(
                            frames_or_frame.data[i: i + largest_write_size]))
                elif isinstance(frames_or_frame, Frame):
                    frames: list[Frame] = [frames_or_frame]
                elif isinstance(frames_or_frame, list):
                    frames: list[Frame] = frames_or_frame
                else:
                    raise Exception("Unknown type in output queue")

                for frame in frames:
                    if isinstance(frame, EndFrame):
                        self._logger.info("Stopping frame consumer thread")
                        self._stop_threads.set()
                        self._threadsafe_send_queue.task_done()
                        if self._loop:
                            asyncio.run_coroutine_threadsafe(
                                self.completed_queue.put(frame), self._loop
                            )
                            # Also send the EndFrame to the pipeline so it can stop
                            asyncio.run_coroutine_threadsafe(
                                self.receive_queue.put(frame), self._loop
                            )
                        return

                    # if interrupted, we just pull frames off the queue and
                    # discard them
                    if not self._is_interrupted.is_set():
                        if frame:
                            if isinstance(frame, AudioFrame):
                                chunk = frame.data

                                b.extend(chunk)
                                truncated_length: int = len(b) - (
                                    len(b) % smallest_write_size
                                )
                                if truncated_length:
                                    self.write_frame_to_mic(
                                        bytes(b[:truncated_length]))
                                    b = b[truncated_length:]
                            elif isinstance(frame, ImageFrame):
                                self._set_image(frame.image)
                            elif isinstance(frame, SpriteFrame):
                                self._set_images(frame.images)
                            elif isinstance(frame, UserImageRequestFrame):
                                self.request_participant_image(frame.user_id)
                            elif isinstance(frame, SendAppMessageFrame):
                                self.send_app_message(frame.message, frame.participant_id)
                        elif len(b):
                            self.write_frame_to_mic(bytes(b))
                            b = bytearray()
                    else:
                        # if there are leftover audio bytes, write them now; failing to do so
                        # can cause static in the audio stream.
                        if len(b):
                            truncated_length = len(b) - (len(b) % 160)
                            self.write_frame_to_mic(
                                bytes(b[:truncated_length]))
                            b = bytearray()

                        if isinstance(frame, StartFrame):
                            self._is_interrupted.clear()
                            asyncio.run_coroutine_threadsafe(
                                self.receive_queue.put(PipelineStartedFrame()),
                                self._loop,
                            )

                    if self._loop:
                        asyncio.run_coroutine_threadsafe(
                            self.completed_queue.put(frame), self._loop
                        )

                self._threadsafe_send_queue.task_done()
            except queue.Empty:
                if len(b):
                    self.write_frame_to_mic(bytes(b))

                b = bytearray()
            except Exception as e:
                self._logger.error(
                    f"Exception in frame_consumer: {e}, {len(b)}")
                raise e
