from dataclasses import dataclass
from typing import Any, List


class Frame:
    def __str__(self):
        return f"{self.__class__.__name__}"


class ControlFrame(Frame):
    # Control frames should contain no instance data, so
    # equality is based solely on the class.
    def __eq__(self, other):
        return isinstance(other, self.__class__)


class StartFrame(ControlFrame):
    """Used (but not required) to start a pipeline, and is also used to
    indicate that an interruption has ended and the transport should start
    processing frames again."""
    pass


class EndFrame(ControlFrame):
    """Indicates that a pipeline has ended and frame processors and pipelines
    should be shut down. If the transport receives this frame, it will stop
    sending frames to its output channel(s) and close all its threads."""
    pass


class EndPipeFrame(ControlFrame):
    """Indicates that a pipeline has ended but that the transport should
    continue processing. This frame is used in parallel pipelines and other
    sub-pipelines."""
    pass


class PipelineStartedFrame(ControlFrame):
    """
    Used by the transport to indicate that execution of a pipeline is starting
    (or restarting). It should be the first frame your app receives when it
    starts, or when an interruptible pipeline has been interrupted.
    """

    pass


class LLMResponseStartFrame(ControlFrame):
    """Used to indicate the beginning of an LLM response. Following TextFrames
    are part of the LLM response until an LLMResponseEndFrame"""
    pass


class LLMResponseEndFrame(ControlFrame):
    """Indicates the end of an LLM response."""
    pass


@dataclass()
class AudioFrame(Frame):
    """A chunk of audio. Will be played by the transport if the transport's mic
    has been enabled."""
    data: bytes

    def __str__(self):
        return f"{self.__class__.__name__}, size: {len(self.data)} B"


@dataclass()
class ImageFrame(Frame):
    """An image. Will be shown by the transport if the transport's camera is
    enabled."""
    image: bytes
    size: tuple[int, int]

    def __str__(self):
        return f"{self.__class__.__name__}, image size: {self.size[0]}x{self.size[1]} buffer size: {len(self.image)} B"


@dataclass()
class URLImageFrame(ImageFrame):
    """An image with an associated URL. Will be shown by the transport if the
    transport's camera is enabled.

    """
    url: str | None

    def __init__(self, url, image, size):
        super().__init__(image, size)
        self.url = url

    def __str__(self):
        return f"{self.__class__.__name__}, url: {self.url}, image size: {self.size[0]}x{self.size[1]}, buffer size: {len(self.image)} B"


@dataclass()
class VisionImageFrame(ImageFrame):
    """An image with an associated text to ask for a description of it. Will be shown by the
    transport if the transport's camera is enabled.

    """
    text: str | None

    def __init__(self, text, image, size):
        super().__init__(image, size)
        self.text = text

    def __str__(self):
        return f"{self.__class__.__name__}, text: {self.text}, image size: {self.size[0]}x{self.size[1]}, buffer size: {len(self.image)} B"


@dataclass()
class UserImageFrame(ImageFrame):
    """An image associated to a user. Will be shown by the transport if the transport's camera is
    enabled."""
    user_id: str

    def __init__(self, user_id, image, size):
        super().__init__(image, size)
        self.user_id = user_id

    def __str__(self):
        return f"{self.__class__.__name__}, user: {self.user_id}, image size: {self.size[0]}x{self.size[1]}, buffer size: {len(self.image)} B"


@dataclass()
class UserImageRequestFrame(Frame):
    """A frame user to request an image from the given user."""
    user_id: str

    def __str__(self):
        return f"{self.__class__.__name__}, user: {self.user_id}"


@dataclass()
class SpriteFrame(Frame):
    """An animated sprite. Will be shown by the transport if the transport's
    camera is enabled. Will play at the framerate specified in the transport's
    `fps` constructor parameter."""
    images: list[bytes]

    def __str__(self):
        return f"{self.__class__.__name__}, list size: {len(self.images)}"


@dataclass()
class TextFrame(Frame):
    """A chunk of text. Emitted by LLM services, consumed by TTS services, can
    be used to send text through pipelines."""
    text: str

    def __str__(self):
        return f'{self.__class__.__name__}: "{self.text}"'


@dataclass()
class TranscriptionFrame(TextFrame):
    """A text frame with transcription-specific data. Will be placed in the
    transport's receive queue when a participant speaks."""
    participantId: str
    timestamp: str

    def __str__(self):
        return f"{self.__class__.__name__}, text: '{self.text}' participantId: {self.participantId}, timestamp: {self.timestamp}"


@dataclass()
class InterimTranscriptionFrame(TextFrame):
    """A text frame with interim transcription-specific data. Will be placed in
    the transport's receive queue when a participant speaks."""
    participantId: str
    timestamp: str

    def __str__(self):
        return f"{self.__class__.__name__}, text: '{self.text}' participantId: {self.participantId}, timestamp: {self.timestamp}"


class TTSStartFrame(ControlFrame):
    """Used to indicate the beginning of a TTS response. Following AudioFrames
    are part of the TTS response until an TTEndFrame. These frames can be used
    for aggregating audio frames in a transport to optimize the size of frames
    sent to the session, without needing to control this in the TTS service."""
    pass


class TTSEndFrame(ControlFrame):
    """Indicates the end of a TTS response."""
    pass


@dataclass()
class LLMMessagesFrame(Frame):
    """A frame containing a list of LLM messages. Used to signal that an LLM
    service should run a chat completion and emit an LLMStartFrames, TextFrames
    and an LLMEndFrame.
    Note that the messages property on this class is mutable, and will be
    be updated by various ResponseAggregator frame processors."""
    messages: List[dict]


@dataclass()
class ReceivedAppMessageFrame(Frame):
    message: Any
    sender: str

    def __str__(self):
        return f"ReceivedAppMessageFrame: sender: {self.sender}, message: {self.message}"


@dataclass()
class SendAppMessageFrame(Frame):
    message: Any
    participant_id: str | None

    def __str__(self):
        return f"SendAppMessageFrame: participant: {self.participant_id}, message: {self.message}"


class UserStartedSpeakingFrame(Frame):
    """Emitted by VAD to indicate that a participant has started speaking.
    This can be used for interruptions or other times when detecting that
    someone is speaking is more important than knowing what they're saying
    (as you will with a TranscriptionFrame)"""
    pass


class UserStoppedSpeakingFrame(Frame):
    """Emitted by the VAD to indicate that a user stopped speaking."""
    pass


class BotStartedSpeakingFrame(Frame):
    pass


class BotStoppedSpeakingFrame(Frame):
    pass


@dataclass()
class LLMFunctionStartFrame(Frame):
    """Emitted when the LLM receives the beginning of a function call
    completion. A frame processor can use this frame to indicate that it should
    start preparing to make a function call, if it can do so in the absence of
    any arguments."""
    function_name: str


@dataclass()
class LLMFunctionCallFrame(Frame):
    """Emitted when the LLM has received an entire function call completion."""
    function_name: str
    arguments: str
