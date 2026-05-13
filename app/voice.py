from pathlib import Path
import pyttsx3


def speak_text(text: str) -> None:
    """
    Read text out loud directly.
    Useful for CLI demo.
    """
    engine = pyttsx3.init()
    engine.setProperty("rate", 165)
    engine.setProperty("volume", 1.0)

    voices = engine.getProperty("voices")
    if voices:
        engine.setProperty("voice", voices[0].id)

    engine.say(text)
    engine.runAndWait()


def text_to_speech_file(text: str, output_path: str = "agent_answer.wav") -> str:
    """
    Save agent answer to a local audio file.
    Useful for Streamlit UI demo.
    """
    output = Path(output_path)

    engine = pyttsx3.init()
    engine.setProperty("rate", 165)
    engine.setProperty("volume", 1.0)

    voices = engine.getProperty("voices")
    if voices:
        engine.setProperty("voice", voices[0].id)

    engine.save_to_file(text, str(output))
    engine.runAndWait()

    return str(output)