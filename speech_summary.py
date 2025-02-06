import os
# import textwrap

# import speech_recognition as sr
from pydub import AudioSegment
# from transformers import pipeline
import nltk
import whisper
import torch
import openai
API_KEY = "sk-"  # Your OpenAI API key here
client = openai.OpenAI(api_key=API_KEY)

# Download necessary NLTK resources
nltk.download('punkt')


def mp3_to_wav(mp3_path, wav_path):
    """Convert MP3 file to WAV format."""
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")


def transcribe_audio(wav_path, language="pl"):
    """Transcribe audio using OpenAI Whisper on GPU if available."""

    print("Loading Whisper model...")
    model = whisper.load_model("medium")  # Choose: tiny, base, small, medium, large

    # 🔹 Detect if a GPU is available and move the model to GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)

    print(f"Processing audio with Whisper on {device} (Language: {language})...")

    # 🔹 Run transcription on GPU (if available)
    result = model.transcribe(wav_path, language=language, fp16=True if device == "cuda" else False)

    return result["text"]




def summarize_text(file_path):
    """Wczytuje plik tekstowy i generuje podsumowanie w punktach"""

    # Odczyt pliku
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Zapytanie do OpenAI GPT-4
    prompt = f"""
    Make a summary of text below, in the same language the text is in:

    {text}

    Summary should be done by extracting most important info into bullet points. 
    It is important that it is in the language text is in, not language the prompt is in.
    Summary length should be about 10% of original text length.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are helpful assistant."},
                      {"role": "user", "content": prompt}],
            temperature=0.3
        )

        summary = response.choices[0].message.content
        return summary

    except Exception as e:
        return f"Błąd: {str(e)}"




def save_text_to_file(text, filename):
    """Save text to a specified file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


def process_audio_file(mp3_path, language, transcription_file="transcription.txt", summary_file="summary.txt"):
    """
    Processes an MP3 file: converts to WAV, transcribes speech, generates an AI summary,
    and saves results into separate files.

    Parameters:
        mp3_path (str): Path to the MP3 file.
        transcription_file (str): File to save the transcription (default: 'transcription.txt').
        summary_file (str): File to save the summary (default: 'summary.txt').

    Returns:
        dict: A dictionary containing 'transcription' and 'summary'.
    """

    if not os.path.exists(mp3_path):
        raise FileNotFoundError(f"Error: File '{mp3_path}' not found!")

    # Use 3 lines below if you want to input mp3 to function
    # wav_path = "converted_audio.wav"

    # print("Converting MP3 to WAV...")
    # mp3_to_wav(mp3_path, wav_path)

    # Use below line to input wav to function
    wav_path = mp3_path

    print("Transcribing audio...")
    transcription = transcribe_audio(wav_path, language=language)

    print(f"Saving transcription to '{transcription_file}'...")
    save_text_to_file(transcription, transcription_file)

    print("Generating AI-powered summary...")
    summary = summarize_text(transcription_file)

    print(f"Saving summary to '{summary_file}'...")
    save_text_to_file(summary, summary_file)

    print(f"\nTranscription saved to {transcription_file}")
    print(f"Summary saved to {summary_file}")

    # Clean up the temporary WAV file ( comment if using wav input )
    # os.remove(wav_path)

    return {"transcription": transcription, "summary": summary}