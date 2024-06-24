import os
import speech_recognition as sr
from pydub import AudioSegment

def convert_mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format='wav')

def transcribe_audio(wav_path, text_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            with open(text_path, 'w') as text_file:
                text_file.write(text)
        print(f'Transcribed audio for {wav_path}')
    except Exception as e:
        print(f'Could not transcribe audio for {wav_path}: {e}')

# Define the path to the folder containing the audio files
audio_folder = 'extracted_audio'

# Create a folder for the transcriptions if it doesn't exist
transcription_folder = 'transcribe_audio2text'
os.makedirs(transcription_folder, exist_ok=True)

# Loop through each audio file in the folder, convert to wav, and transcribe
for audio_file in os.listdir(audio_folder):
    if audio_file.endswith('.mp3'):
        mp3_path = os.path.join(audio_folder, audio_file)
        wav_path = os.path.join(audio_folder, os.path.splitext(audio_file)[0] + '.wav')
        
        # Convert mp3 to wav
        convert_mp3_to_wav(mp3_path, wav_path)
        
        # Transcribe wav file
        text_path = os.path.join(transcription_folder, os.path.splitext(audio_file)[0] + '.txt')
        transcribe_audio(wav_path, text_path)

        # Optionally, you can delete the wav file after transcription to save space
        os.remove(wav_path)