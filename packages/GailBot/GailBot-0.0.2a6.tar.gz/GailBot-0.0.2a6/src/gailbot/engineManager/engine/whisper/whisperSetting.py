from pydantic import BaseModel

from gailbot.configs import whisper_config_loader


class WhisperSetting(BaseModel):
    engine: str
    language: str
    detect_speakers: bool = False

    @staticmethod
    def predefined_config():
        config = whisper_config_loader()
        return config
 