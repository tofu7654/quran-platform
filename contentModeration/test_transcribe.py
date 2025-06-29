import os
from dotenv import load_dotenv
from openai import OpenAI

# ✅ Load .env for API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Common Quranic Keywords
QURAN_KEYWORDS = [
    "الله", "الرحمن", "الرحيم", "سورة", "آية",
    "قال", "يوم", "كتاب", "الذين", "جنة", "نار", "رب", "الملك", "العرش"
]

# ✅ 1️⃣ Transcription
def transcribe_arabic_audio(file_path: str) -> str:
    """
    Transcribes Arabic audio using OpenAI Whisper.
    """
    print("\n🎤 Transcribing audio with Whisper...")
    with open("test-recording.mp3", "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="ar",           # Force Arabic output
            temperature=0
        )
    print("✅ Transcription complete.\n")
    return transcript.text.strip()

# ✅ 2️⃣ Heuristic Keyword Check
def heuristic_is_quran(text: str) -> bool:
    """
    Checks for Quranic keywords in Arabic text.
    """
    for keyword in QURAN_KEYWORDS:
        if keyword in text:
            print(f"✅ Heuristic match found: '{keyword}'")
            return True
    return False

# ✅ 3️⃣ ChatGPT Classifier
def classify_as_quran_or_not(text: str) -> str:
    """
    Uses ChatGPT to classify text as Quran or Not Quran.
    """
    print("\n🤖 Calling ChatGPT for classification...")

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

    response = client.chat.completions.create(
        model="gpt-4o",  # Or use gpt-3.5-turbo if cheaper
        messages=[
            {"role": "system", "content": "You are a text classifier."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip().lower()
    print(f"✅ ChatGPT Classification Response: '{result}'")
    return result

# ✅ 4️⃣ Combined Check
def is_quranic_text(transcribed_text: str) -> bool:
    """
    Combined heuristic + ChatGPT approach.
    """
    # Heuristic first
    if heuristic_is_quran(transcribed_text):
        print("\n✅ FINAL DECISION: Quran (via heuristics)")
        return True

    # Fallback to GPT classification
    classification = classify_as_quran_or_not(transcribed_text)
    if "quran" in classification:
        print("\n✅ FINAL DECISION: Quran (via ChatGPT)")
        return True
    else:
        print("\n❌ FINAL DECISION: Not Quran")
        return False

# ✅ 5️⃣ Main test runner
if __name__ == "__main__":
    AUDIO_PATH = "test_quran.mp3"  # Replace with your test file

    print("🔎 Testing Quran Audio Verification Pipeline\n")
    print(f"📂 Audio file: {AUDIO_PATH}")

    try:
        # Step 1: Transcribe
        transcription = transcribe_arabic_audio(AUDIO_PATH)
        print("\n📝 Transcription Result:\n")
        print(transcription)

        # Step 2: Classification
        is_quran = is_quranic_text(transcription)
        print("\n🌟 Verdict:", "QURAN ✅" if is_quran else "NOT QURAN ❌")

    except Exception as e:
        print("\n❌ ERROR:", str(e))
