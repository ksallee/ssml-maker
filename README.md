# SSML Maker

A Python library for building SSML (Speech Synthesis Markup Language) documents with a fluent interface.

## Installation

```bash
pip install ssml-maker
```

## Features

- Fluent interface for building SSML documents
- Support for all major SSML elements
- Type hints and proper documentation
- Comprehensive test coverage
- Input validation and error handling

## Quick Start

```python
from ssml_maker import Speech, InterpretAs, ProsodyConfig, ProsodyRate

# Create a simple SSML document
with Speech() as speech:
    speech.add_text("Here are ")
    with speech.say_as(InterpretAs.CHARACTERS):
        speech.add_text("SSML")
    speech.add_text(" examples")

# Get the SSML string
ssml_string = speech.build()
print(ssml_string)
```

## Advanced Usage

### Prosody Control

```python
from ssml_maker import ProsodyConfig, ProsodyRate, ProsodyPitch, VolumeLevel

config = ProsodyConfig(
    rate=ProsodyRate.FAST,
    pitch=ProsodyPitch.HIGH,
    volume=VolumeLevel.LOUD
)

with Speech() as speech:
    with speech.prosody(config):
        speech.add_text("This will be spoken quickly, with high pitch and loud volume")
```

### Voice Selection

```python
with Speech() as speech:
    with speech.voice(name="Joanna", language="en-US", gender="female"):
        speech.add_text("This text will be spoken by Joanna")
```

### Phonetic Pronunciation

```python
from ssml_maker import PhoneticAlphabet

with Speech() as speech:
    with speech.phoneme(PhoneticAlphabet.IPA, "pɪˈkɑːn"):
        speech.add_text("pecan")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.