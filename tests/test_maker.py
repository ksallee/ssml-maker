import pytest
from ssml_maker import Speech, InterpretAs, ProsodyConfig, ProsodyRate, ProsodyPitch, VolumeLevel, EmphasisLevel, \
    BreakStrength, PhoneticAlphabet


def test_empty_speech():
    speech = Speech()
    assert speech.build() == "<speak></speak>"


def test_text_escaping():
    speech = Speech()
    speech.add_text("Hello & Goodbye <test>")
    assert "Hello &amp; Goodbye &lt;test&gt;" in speech.build()


def test_simple_nesting():
    with Speech() as speech:
        with speech.voice(name="Joanna"):
            speech.add_text("Hello world")
    assert '<voice name="Joanna">Hello world</voice>' in speech.build()


def test_say_as_element():
    with Speech() as speech:
        with speech.say_as(InterpretAs.CHARACTERS):
            speech.add_text("ABC")
    assert '<say-as interpret-as="characters">ABC</say-as>' in speech.build()


@pytest.mark.parametrize("rate,pitch,volume,expected", [
    (ProsodyRate.FAST, ProsodyPitch.HIGH, VolumeLevel.LOUD,
     '<prosody rate="fast" pitch="high" volume="loud">'),
    ("+20%", "-5st", "+3dB",
     '<prosody rate="+20%" pitch="-5st" volume="+3dB">'),
])
def test_prosody_element(rate, pitch, volume, expected):
    config = ProsodyConfig(rate=rate, pitch=pitch, volume=volume)
    with Speech() as speech:
        with speech.prosody(config):
            speech.add_text("Test")
    assert expected in speech.build()


def test_prosody_validation():
    with pytest.raises(ValueError):
        config = ProsodyConfig(rate="invalid")
        with Speech() as speech:
            with speech.prosody(config):
                speech.add_text("Test")


def test_break_element():
    with Speech() as speech:
        speech.add_break(time="3s")
        speech.add_break(strength=BreakStrength.STRONG)
    assert '<break time="3s"/>' in speech.build()
    assert '<break strength="strong"/>' in speech.build()


def test_break_validation():
    with pytest.raises(ValueError):
        with Speech() as speech:
            speech.add_break()  # No params


def test_audio_element():
    with Speech() as speech:
        with speech.audio(src="test.mp3", clip_begin="1s", speed="150%"):
            speech.add_text("Fallback")
    assert '<audio src="test.mp3" clipBegin="1s" speed="150%">' in speech.build()


def test_sub_element():
    with Speech() as speech:
        with speech.sub(alias="World Wide Web"):
            speech.add_text("WWW")
    assert '<sub alias="World Wide Web">WWW</sub>' in speech.build()


def test_phoneme_element():
    with Speech() as speech:
        with speech.phoneme(PhoneticAlphabet.IPA, "pɪˈkɑːn"):
            speech.add_text("pecan")
    assert '<phoneme alphabet="ipa" ph="pɪˈkɑːn">pecan</phoneme>' in speech.build()


def test_emphasis_element():
    with Speech() as speech:
        with speech.emphasis(EmphasisLevel.STRONG):
            speech.add_text("Important")
    assert '<emphasis level="strong">Important</emphasis>' in speech.build()


def test_paragraph_structure():
    with Speech() as speech:
        with speech.paragraph():
            with speech.sentence():
                speech.add_text("First")
            with speech.sentence():
                speech.add_text("Second")
    assert "<p><s>First</s><s>Second</s></p>" in speech.build()


def test_mark_element():
    with Speech() as speech:
        speech.mark("chapter1")
    assert '<mark name="chapter1"/>' in speech.build()


def test_lang_element():
    with Speech() as speech:
        with speech.lang("fr-FR"):
            speech.add_text("Bonjour")
    assert '<lang xml:lang="fr-FR">Bonjour</lang>' in speech.build()


def test_style_element():
    with Speech() as speech:
        with speech.style("lively"):
            speech.add_text("Exciting!")
    assert '<google:style name="lively">Exciting!</google:style>' in speech.build()


def test_complex_nesting():
    with Speech() as speech:
        with speech.voice(language="en-US", gender="female"):
            speech.add_text("Main content")
            with speech.prosody(ProsodyConfig(rate=ProsodyRate.SLOW)):
                speech.add_text("Slow speech")
                speech.add_break(time="500ms")
            with speech.emphasis(EmphasisLevel.MODERATE):
                speech.add_text("Important point")
    assert "<voice" in speech.build()
    assert "<prosody rate=\"slow\"" in speech.build()
    assert "<break time=\"500ms\"/>" in speech.build()
    assert "<emphasis level=\"moderate\">" in speech.build()


def test_error_handling():
    # Test invalid voice parameters
    with pytest.raises(ValueError):
        with Speech() as speech:
            with speech.voice():  # No parameters
                pass
    # Test invalid say-as format
    with pytest.raises(ValueError):
        config = ProsodyConfig(rate="invalid_rate")
        with Speech() as speech:
            with speech.prosody(config):
                pass


def test_full_integration():
    expected = """<speak><voice name="Joanna"><prosody rate="fast" pitch="high" volume="loud">Hello<break time="500ms"/><say-as interpret-as="characters">WWW</say-as></prosody></voice></speak>"""

    with Speech() as speech:
        with speech.voice(name="Joanna"):
            with speech.prosody(ProsodyConfig(
                    rate=ProsodyRate.FAST,
                    pitch=ProsodyPitch.HIGH,
                    volume=VolumeLevel.LOUD
            )):
                speech.add_text("Hello")
                speech.add_break(time="500ms")
                with speech.say_as(InterpretAs.CHARACTERS):
                    speech.add_text("WWW")

    assert speech.build() == expected
