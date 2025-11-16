"""
Audio Format Converter
Converts between different audio formats with quality preservation
"""

from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class AudioCodec(Enum):
    """Audio codec types"""
    MP3_CBR = "mp3_cbr"  # Constant bitrate
    MP3_VBR = "mp3_vbr"  # Variable bitrate
    AAC_LC = "aac_lc"    # Low complexity
    AAC_HE = "aac_he"    # High efficiency
    OPUS = "opus"
    VORBIS = "vorbis"
    FLAC = "flac"
    PCM = "pcm"


@dataclass
class ConversionConfig:
    """Configuration for format conversion"""
    output_format: str
    codec: Optional[AudioCodec] = None
    bitrate_kbps: int = 128
    sample_rate: int = 44100
    channels: int = 2  # 1=mono, 2=stereo
    quality: int = 5  # 0-9, where 9 is best
    normalize_audio: bool = True


@dataclass
class ConversionResult:
    """Result from format conversion"""
    success: bool
    converted_audio: Optional[bytes]
    input_format: str
    output_format: str
    input_size: int
    output_size: int
    compression_ratio: float
    duration_ms: float
    error: Optional[str] = None


class FormatConverter:
    """
    Audio format converter with quality optimization

    Supported formats:
    - Input: MP3, WAV, OGG, FLAC, M4A, AAC
    - Output: MP3, WAV, OGG, FLAC, M4A, AAC, OPUS
    """

    # Format extensions and MIME types
    FORMAT_INFO = {
        'mp3': {'mime': 'audio/mpeg', 'extension': '.mp3'},
        'wav': {'mime': 'audio/wav', 'extension': '.wav'},
        'ogg': {'mime': 'audio/ogg', 'extension': '.ogg'},
        'flac': {'mime': 'audio/flac', 'extension': '.flac'},
        'm4a': {'mime': 'audio/mp4', 'extension': '.m4a'},
        'aac': {'mime': 'audio/aac', 'extension': '.aac'},
        'opus': {'mime': 'audio/opus', 'extension': '.opus'}
    }

    # Recommended bitrates for different formats
    RECOMMENDED_BITRATES = {
        'mp3': 192,
        'aac': 128,
        'opus': 96,
        'ogg': 128,
        'flac': 0,  # Lossless
        'wav': 0    # Uncompressed
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def convert(self, audio_data: bytes, input_format: str,
                config: ConversionConfig) -> ConversionResult:
        """
        Convert audio to different format

        Args:
            audio_data: Input audio data
            input_format: Current format
            config: Conversion configuration

        Returns:
            ConversionResult with converted audio
        """
        import time
        start_time = time.time()

        try:
            # Validate input
            if not self._is_format_supported(input_format):
                return self._error_result(input_format, config.output_format,
                                         len(audio_data), start_time,
                                         f"Unsupported input format: {input_format}")

            if not self._is_format_supported(config.output_format):
                return self._error_result(input_format, config.output_format,
                                         len(audio_data), start_time,
                                         f"Unsupported output format: {config.output_format}")

            # In production, use ffmpeg or pydub:
            # from pydub import AudioSegment
            # audio = AudioSegment.from_file(audio_data, format=input_format)
            # audio = audio.set_frame_rate(config.sample_rate)
            # audio = audio.set_channels(config.channels)
            # converted = audio.export(format=config.output_format,
            #                          bitrate=f"{config.bitrate_kbps}k")

            self.logger.info(f"Converting {input_format} -> {config.output_format} "
                           f"({config.bitrate_kbps}kbps, {config.sample_rate}Hz)")

            # Simulate conversion
            converted_data = self._simulate_conversion(audio_data, input_format, config)

            duration_ms = (time.time() - start_time) * 1000
            input_size = len(audio_data)
            output_size = len(converted_data)
            compression_ratio = input_size / output_size if output_size > 0 else 1.0

            return ConversionResult(
                success=True,
                converted_audio=converted_data,
                input_format=input_format,
                output_format=config.output_format,
                input_size=input_size,
                output_size=output_size,
                compression_ratio=compression_ratio,
                duration_ms=duration_ms
            )

        except Exception as e:
            self.logger.error(f"Conversion failed: {e}")
            return self._error_result(input_format, config.output_format,
                                     len(audio_data), start_time, str(e))

    def convert_to_podcast_format(self, audio_data: bytes, input_format: str) -> ConversionResult:
        """
        Convert audio to podcast-optimized format (MP3 @ 128kbps, 44.1kHz, stereo)

        Args:
            audio_data: Input audio
            input_format: Current format

        Returns:
            ConversionResult
        """
        config = ConversionConfig(
            output_format='mp3',
            codec=AudioCodec.MP3_VBR,
            bitrate_kbps=128,
            sample_rate=44100,
            channels=2,
            quality=7,
            normalize_audio=True
        )
        return self.convert(audio_data, input_format, config)

    def convert_to_streaming_format(self, audio_data: bytes, input_format: str) -> ConversionResult:
        """
        Convert to streaming-optimized format (AAC @ 96kbps, 44.1kHz)

        Args:
            audio_data: Input audio
            input_format: Current format

        Returns:
            ConversionResult
        """
        config = ConversionConfig(
            output_format='aac',
            codec=AudioCodec.AAC_HE,
            bitrate_kbps=96,
            sample_rate=44100,
            channels=2,
            quality=6
        )
        return self.convert(audio_data, input_format, config)

    def convert_to_archive_format(self, audio_data: bytes, input_format: str) -> ConversionResult:
        """
        Convert to lossless archive format (FLAC)

        Args:
            audio_data: Input audio
            input_format: Current format

        Returns:
            ConversionResult
        """
        config = ConversionConfig(
            output_format='flac',
            codec=AudioCodec.FLAC,
            sample_rate=48000,
            channels=2,
            quality=8
        )
        return self.convert(audio_data, input_format, config)

    def _is_format_supported(self, format: str) -> bool:
        """Check if format is supported"""
        return format.lower() in self.FORMAT_INFO

    def _simulate_conversion(self, audio_data: bytes, input_format: str,
                           config: ConversionConfig) -> bytes:
        """Simulate format conversion"""
        # Estimate output size based on bitrate
        # Assuming 3 minutes of audio
        estimated_duration_sec = 180
        estimated_size = int((config.bitrate_kbps * 1000 / 8) * estimated_duration_sec)

        return b'\x00' * estimated_size

    def _error_result(self, input_format: str, output_format: str,
                     input_size: int, start_time: float, error: str) -> ConversionResult:
        """Create error result"""
        return ConversionResult(
            success=False,
            converted_audio=None,
            input_format=input_format,
            output_format=output_format,
            input_size=input_size,
            output_size=0,
            compression_ratio=0.0,
            duration_ms=(time.time() - start_time) * 1000,
            error=error
        )

    def get_supported_formats(self) -> list[str]:
        """Get list of supported formats"""
        return list(self.FORMAT_INFO.keys())

    def get_format_info(self, format: str) -> Optional[Dict]:
        """Get information about a format"""
        return self.FORMAT_INFO.get(format.lower())

    def get_recommended_bitrate(self, format: str) -> int:
        """Get recommended bitrate for a format"""
        return self.RECOMMENDED_BITRATES.get(format.lower(), 128)
