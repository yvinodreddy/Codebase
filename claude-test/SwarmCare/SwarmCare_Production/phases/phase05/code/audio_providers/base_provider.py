"""
Base Audio Provider
Abstract base class for all TTS providers
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class AudioFormat(Enum):
    """Supported audio formats"""
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"
    FLAC = "flac"
    AAC = "aac"


class VoiceGender(Enum):
    """Voice gender options"""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"


@dataclass
class VoiceProfile:
    """Voice configuration profile"""
    provider: str
    voice_id: str
    voice_name: str
    language: str
    gender: VoiceGender
    neural: bool = True
    sample_rate: int = 24000
    speaking_rate: float = 1.0
    pitch: float = 0.0
    volume: float = 1.0


@dataclass
class AudioGenerationRequest:
    """Request for audio generation"""
    text: str
    voice_profile: VoiceProfile
    output_format: AudioFormat = AudioFormat.MP3
    quality: str = "high"
    enable_ssml: bool = False
    metadata: Optional[Dict] = None


@dataclass
class AudioGenerationResponse:
    """Response from audio generation"""
    success: bool
    audio_data: Optional[bytes]
    duration_seconds: float
    file_size_bytes: int
    format: AudioFormat
    sample_rate: int
    provider: str
    voice_used: str
    error: Optional[str] = None
    metadata: Optional[Dict] = None


class BaseAudioProvider(ABC):
    """
    Abstract base class for audio generation providers
    All TTS providers must implement this interface
    """

    def __init__(self, config: Dict):
        self.config = config
        self.provider_name = "base"
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @abstractmethod
    def generate_audio(self, request: AudioGenerationRequest) -> AudioGenerationResponse:
        """
        Generate audio from text

        Args:
            request: Audio generation request with text and configuration

        Returns:
            AudioGenerationResponse with audio data or error
        """
        pass

    @abstractmethod
    def get_available_voices(self, language: Optional[str] = None) -> List[VoiceProfile]:
        """
        Get list of available voices

        Args:
            language: Optional language filter (e.g., 'en-US')

        Returns:
            List of available voice profiles
        """
        pass

    @abstractmethod
    def validate_voice(self, voice_id: str) -> bool:
        """
        Validate if a voice ID is available

        Args:
            voice_id: Voice identifier to validate

        Returns:
            True if voice is available, False otherwise
        """
        pass

    def get_estimated_cost(self, text: str) -> float:
        """
        Estimate cost for generating audio

        Args:
            text: Text to convert to speech

        Returns:
            Estimated cost in USD
        """
        # Default implementation - override in subclasses
        character_count = len(text)
        # Average: $4 per 1M characters for neural voices
        return (character_count / 1_000_000) * 4.0

    def supports_ssml(self) -> bool:
        """Check if provider supports SSML"""
        return True

    def supports_format(self, format: AudioFormat) -> bool:
        """Check if provider supports audio format"""
        return True

    def get_max_text_length(self) -> int:
        """Get maximum text length supported"""
        return 5000  # Default 5000 characters

    def validate_request(self, request: AudioGenerationRequest) -> tuple[bool, Optional[str]]:
        """
        Validate audio generation request

        Args:
            request: Request to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not request.text or len(request.text.strip()) == 0:
            return False, "Text cannot be empty"

        if len(request.text) > self.get_max_text_length():
            return False, f"Text exceeds maximum length of {self.get_max_text_length()} characters"

        if not self.supports_format(request.output_format):
            return False, f"Format {request.output_format.value} not supported by this provider"

        if request.enable_ssml and not self.supports_ssml():
            return False, "SSML not supported by this provider"

        return True, None
