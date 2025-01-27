from enum import Enum
from dataclasses import dataclass
import html
import re
from typing import List, Optional, Union


class InterpretAs(str, Enum):
    """Valid values for the interpret-as attribute of <say-as>"""
    CHARACTERS = "characters"
    SPELL_OUT = "spell-out"
    CARDINAL = "cardinal"
    NUMBER = "number"
    ORDINAL = "ordinal"
    DIGITS = "digits"
    FRACTION = "fraction"
    UNIT = "unit"
    DATE = "date"
    TIME = "time"
    TELEPHONE = "telephone"
    ADDRESS = "address"
    INTERJECTION = "interjection"
    EXPLETIVE = "expletive"
    VERBATIM = "verbatim"
    DURATION = "duration"


class ProsodyRate(str, Enum):
    """Predefined values for prosody rate attribute"""
    X_SLOW = "x-slow"
    SLOW = "slow"
    MEDIUM = "medium"
    FAST = "fast"
    X_FAST = "x-fast"


class ProsodyPitch(str, Enum):
    """Predefined values for prosody pitch attribute"""
    X_LOW = "x-low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    X_HIGH = "x-high"


class VolumeLevel(str, Enum):
    """Valid values for prosody volume attribute"""
    SILENT = "silent"
    X_SOFT = "x-soft"
    SOFT = "soft"
    MEDIUM = "medium"
    LOUD = "loud"
    X_LOUD = "x-loud"


class EmphasisLevel(str, Enum):
    """Valid values for emphasis level attribute"""
    STRONG = "strong"
    MODERATE = "moderate"
    REDUCED = "reduced"
    NONE = "none"


class BreakStrength(str, Enum):
    """Valid values for break strength attribute"""
    X_WEAK = "x-weak"
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"
    X_STRONG = "x-strong"
    NONE = "none"


class PhoneticAlphabet(str, Enum):
    """Valid phonetic alphabet types"""
    IPA = "ipa"
    X_SAMPA = "x-sampa"
    YOMIGANA = "yomigana"
    PINYIN = "pinyin"
    JYUTPING = "jyutping"


@dataclass
class ProsodyConfig:
    """Configuration container for prosody attributes"""
    rate: Union[ProsodyRate, str] = ProsodyRate.MEDIUM
    pitch: Union[ProsodyPitch, str] = ProsodyPitch.MEDIUM
    volume: Union[VolumeLevel, str] = VolumeLevel.MEDIUM


class Speech:
    """Main SSML builder class providing fluent interface for constructing SSML documents"""

    def __init__(self):
        self._elements: List[str] = []
        self._stack: List[str] = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._stack:
            self._elements.append(self._stack.pop())

    def build(self) -> str:
        """Finalizes and returns the complete SSML document

        :return: Complete SSML string wrapped in <speak> tags
        """
        return f"<speak>{''.join(self._elements)}</speak>"

    def add_text(self, text: str) -> "Speech":
        """Adds escaped text content to the SSML document

        :param text: Text content to add
        :return: Self instance for method chaining
        """
        self._elements.append(html.escape(text))
        return self

    def _add_tag(self, tag: str, attributes: Optional[dict] = None) -> "Speech":
        """Base method for adding XML tags with attributes

        :param tag: The XML tag name to add
        :param attributes: Dictionary of attribute key-value pairs
        :return: Self instance for method chaining
        """
        attrs = " ".join(f'{k}="{v}"' for k, v in (attributes or {}).items())
        self._elements.append(f"<{tag}{' ' + attrs if attrs else ''}>")
        self._stack.append(f"</{tag}>")
        return self

    # SSML Elements Implementation
    def say_as(self, interpret_as: InterpretAs, format: Optional[str] = None,
               detail: Optional[str] = None) -> "Speech":
        """Context manager for <say-as> element

        :param interpret_as: Interpretation style from InterpretAs enum
        :param format: Optional format specification
        :param detail: Optional detail level specification
        :return: Self instance for method chaining
        :raises ValueError: If interpret_as is invalid
        """
        attrs = {"interpret-as": interpret_as.value}
        if format:
            attrs["format"] = format
        if detail:
            attrs["detail"] = detail
        return self._add_tag("say-as", attrs)

    def prosody(self, config: ProsodyConfig) -> "Speech":
        """Context manager for <prosody> element

        :param config: Prosody configuration dataclass
        :return: Self instance for method chaining
        :raises ValueError: If any prosody attribute is invalid
        """
        # Validate rate
        print("CONFIG RATE", config.rate)
        print("match", re.match(r"^[+-]?\d+%$", config.rate))
        if isinstance(config.rate, ProsodyRate):
            rate = config.rate.value
        elif re.match(r"^[+-]?\d+%$", config.rate):
            rate = config.rate
        else:
            raise ValueError("Invalid prosody rate value")

        # Validate pitch
        if isinstance(config.pitch, ProsodyPitch):
            pitch = config.pitch.value
        elif re.match(r"^[+-]?\d+(\.\d+)?(st|%)$", config.pitch):
            pitch = config.pitch
        else:
            raise ValueError("Invalid prosody pitch value")

        # Validate volume
        if isinstance(config.volume, VolumeLevel):
            volume = config.volume.value
        elif re.match(r"^[+-]?\d+(\.\d+)?dB$", config.volume):
            volume = config.volume
        else:
            raise ValueError("Invalid prosody volume value")

        return self._add_tag("prosody", {"rate": rate, "pitch": pitch, "volume": volume})

    def add_break(self, time: Optional[str] = None, strength: Optional[BreakStrength] = None) -> "Speech":
        """Adds a <break> element

        :param time: Duration specification (e.g., "3s", "250ms")
        :param strength: Break strength from BreakStrength enum
        :return: Self instance for method chaining
        :raises ValueError: If neither time nor strength provided or invalid format
        """
        if not time and not strength:
            raise ValueError("Either time or strength must be provided")

        attrs = {}
        if time:
            if not re.match(r"^\d+(\.\d+)?(s|ms)$", time):
                raise ValueError("Invalid break time format")
            attrs["time"] = time
        if strength:
            attrs["strength"] = strength.value
        to_append = ' '.join(f'{k}="{v}"' for k, v in attrs.items())
        self._elements.append(f"<break {to_append}/>")
        return self

    def voice(self, name: Optional[str] = None, language: Optional[str] = None,
              gender: Optional[str] = None, variant: Optional[str] = None) -> "Speech":
        """Context manager for <voice> element

        :param name: Voice name identifier
        :param language: BCP-47 language code
        :param gender: Voice gender ("male", "female", "neutral")
        :param variant: Voice variant identifier
        :return: Self instance for method chaining
        :raises ValueError: If no parameters provided
        """
        attrs = {}
        if name:
            attrs["name"] = name
        if language:
            attrs["xml:lang"] = language
        if gender:
            attrs["gender"] = gender
        if variant:
            attrs["variant"] = variant

        if not attrs:
            raise ValueError("At least one voice parameter must be provided")

        return self._add_tag("voice", attrs)

    def audio(self, src: str, clip_begin: Optional[str] = None, clip_end: Optional[str] = None,
              speed: Optional[str] = None, repeat_count: Optional[int] = None,
              repeat_dur: Optional[str] = None, sound_level: Optional[str] = None) -> "Speech":
        """Context manager for <audio> element

        :param src: Required audio source URL
        :param clip_begin: Time offset to start playback
        :param clip_end: Time offset to end playback
        :param speed: Playback speed percentage (e.g., "150%")
        :param repeat_count: Number of times to repeat
        :param repeat_dur: Total duration for repetitions
        :param sound_level: Volume adjustment in dB (e.g., "+6dB")
        :return: Self instance for method chaining
        :raises ValueError: If src is not provided
        """
        attrs = {"src": src}
        if clip_begin:
            attrs["clipBegin"] = clip_begin
        if clip_end:
            attrs["clipEnd"] = clip_end
        if speed:
            attrs["speed"] = speed
        if repeat_count:
            attrs["repeatCount"] = str(repeat_count)
        if repeat_dur:
            attrs["repeatDur"] = repeat_dur
        if sound_level:
            attrs["soundLevel"] = sound_level

        return self._add_tag("audio", attrs)

    def sub(self, alias: str) -> "Speech":
        """Context manager for <sub> element

        :param alias: Replacement text for pronunciation
        :return: Self instance for method chaining
        """
        return self._add_tag("sub", {"alias": alias})

    def lang(self, language_code: str) -> "Speech":
        """Context manager for <lang> element

        :param language_code: BCP-47 language code
        :return: Self instance for method chaining
        """
        return self._add_tag("lang", {"xml:lang": language_code})

    def phoneme(self, alphabet: PhoneticAlphabet, ph: str) -> "Speech":
        """Context manager for <phoneme> element

        :param alphabet: Phonetic alphabet type from PhoneticAlphabet
        :param ph: Phonetic pronunciation string
        :return: Self instance for method chaining
        """
        return self._add_tag("phoneme", {"alphabet": alphabet.value, "ph": ph})

    def emphasis(self, level: EmphasisLevel) -> "Speech":
        """Context manager for <emphasis> element

        :param level: Emphasis level from EmphasisLevel
        :return: Self instance for method chaining
        """
        return self._add_tag("emphasis", {"level": level.value})

    def paragraph(self) -> "Speech":
        """Context manager for <p> (paragraph) element

        :return: Self instance for method chaining
        """
        return self._add_tag("p")

    def sentence(self) -> "Speech":
        """Context manager for <s> (sentence) element

        :return: Self instance for method chaining
        """
        return self._add_tag("s")

    def mark(self, name: str) -> "Speech":
        """Adds a <mark> element

        :param name: Unique identifier for the mark
        :return: Self instance for method chaining
        """
        self._elements.append(f'<mark name="{html.escape(name)}"/>')
        return self

    def style(self, name: str) -> "Speech":
        """Context manager for <google:style> element

        :param name: Style name (e.g., "lively", "calm")
        :return: Self instance for method chaining
        """
        return self._add_tag("google:style", {"name": name})


# Example usage
if __name__ == "__main__":
    speech = Speech()
    with speech:
        speech.add_text("Here are ")
        with speech.say_as(InterpretAs.CHARACTERS):
            speech.add_text("SSML")
        speech.add_text(" samples. I can pause ")
        speech.add_break(time="3s")
        speech.add_text(". I can play a sound")
        with speech.audio(src="https://example.com/sound.mp3"):
            speech.add_text("fallback text")
        with speech.paragraph():
            with speech.sentence():
                speech.add_text("This is sentence one.")
            with speech.sentence():
                speech.add_text("This is sentence two.")

    print(speech.build())