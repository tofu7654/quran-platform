import os
import tempfile
from dotenv import load_dotenv
from openai import AsyncOpenAI
import logging

# ✅ Load your .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

logger = logging.getLogger(__name__)

# ✅ Quranic Arabic Keywords for Heuristics
QURAN_KEYWORDS = [
    "الله", "الرحمن", "الرحيم", "سورة", "آية",
    "قال", "يوم", "كتاب", "الذين", "جنة", "نار", "رب", "الملك", "العرش"
]

# ✅ Transcription function
async def transcribe_audio(file_bytes: bytes) -> str:
    """
    Transcribes Arabic audio using Whisper via OpenAI.
    """
    logger.info("🎤 Starting transcription with Whisper...")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(file_bytes)
        tmp.flush()
        audio_file = open(tmp.name, "rb")
        response = await client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="ar",
            temperature=0
        )
        transcription = response.text.strip().lower()

    logger.info(f"✅ Transcription complete: {transcription[:60]}...")
    return transcription

# ✅ Heuristic filter
def heuristic_is_quran(text: str) -> bool:
    """
    Checks for Quranic keywords in Arabic text.
    """
    for keyword in QURAN_KEYWORDS:
        if keyword in text:
            logger.info(f"✅ Heuristic match found: '{keyword}'")
            return True
    return False

# ✅ ChatGPT classification
async def classify_as_quran_or_not(text: str) -> bool:
    """
    Uses ChatGPT to classify text as Quran or Not Quran.
    """
    logger.info("🤖 Calling ChatGPT for classification...")

    prompt = (
        "You are an expert at recognizing Quranic Arabic text, even if it is partial, "
        "contains errors, or has background noise artifacts. Your job is to classify "
        "text as 'Quran' if it is even *likely* to be Quranic Arabic or a verse from the Quran. "
        "If it is definitely not from the Quran, reply with 'Not Quran'.\n\n"
        "Examples:\n\n"
        "Text: 'بسم الله الرحمن الرحيم'\nClassification: Quran\n"
        "Text: 'الحمد لله رب العالمين'\nClassification: Quran\n"
        "Text: 'هذا تسجيل صوتي تجريبي'\nClassification: Not Quran\n"
        "Text: 'الله اكبر الرحمن الرحيم'\nClassification: Quran\n\n"
        f"Now classify this text:\n\n{text}\n\nClassification:"
    )

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a text classifier."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip().lower()
    logger.info(f"✅ ChatGPT Classification Response: '{result}'")
    return "quran" in result

# ✅ Combined moderation check
async def verify_audio_is_quran(file_bytes: bytes) -> bool:
    """
    Full moderation pipeline:
    1. Transcribe audio to Arabic text
    2. Check heuristics
    3. Fallback to ChatGPT classification
    """
    try:
        # Step 1: Transcribe
        transcription = await transcribe_audio(file_bytes)

        # Step 2: Heuristic check
        if heuristic_is_quran(transcription):
            logger.info("✅ FINAL DECISION: Quran (via heuristics)")
            return True

        # Step 3: ChatGPT fallback
        is_quran = await classify_as_quran_or_not(transcription)
        if is_quran:
            logger.info("✅ FINAL DECISION: Quran (via ChatGPT)")
        else:
            logger.info("❌ FINAL DECISION: Not Quran")
        return is_quran

    except Exception as e:
        logger.error(f"❌ Error in moderation pipeline: {str(e)}")
        return False
