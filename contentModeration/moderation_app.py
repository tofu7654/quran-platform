import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def transcribe_audio(file_bytes: bytes) -> str:
    import tempfile

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(file_bytes)
        tmp.flush()

        audio_file = open(tmp.name, "rb")
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="ar",
            temperature=0
        )
        return transcript.text.lower()

async def classify_as_quran_or_not(transcribed_text: str) -> bool:
    """
    Uses ChatGPT to decide if the text is Quran or not.
    Returns True if it is Quranic, False otherwise.
    """
    prompt = (
        "You are a helpful assistant that checks if a given text is from the Quran. "
        "If the text is a Quranic verse reply only with 'Quran'. "
        "If it is not from the Quran, reply only with 'Not Quran'.\n\n"
        f"Text:\n{transcribed_text}"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a text classifier."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip().lower()
    return result == "quran" 

