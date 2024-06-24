import os
from textblob import TextBlob
from concurrent.futures import ThreadPoolExecutor
import time
from googletrans import Translator  # Explicitly import Translator

def translate_text(text_path, output_dir, target_language="es"):
    try:
        with open(text_path, "r") as file:
            text = file.read()

        # Use GoogleTrans Translator explicitly
        translator = Translator()
        translated_text = translator.translate(text, dest=target_language).text
        
        filename = os.path.basename(text_path).split('.')[0]
        translation_path = os.path.join(output_dir, f"{filename}_translated.txt")
        
        with open(translation_path, "w") as file:
            file.write(translated_text)
        
        print(f"Translated text saved to {translation_path}")
    except Exception as e:
        print(f"Error translating {text_path}: {e}")

def main():
    transcriptions_dir = "transcribe_audio2text"  # Folder containing text files for analysis
    output_dir = "translations"  # Directory to save translated files
    
    if not os.path.exists(transcriptions_dir):
        print(f"The directory {transcriptions_dir} does not exist.")
        return

    # Create translations directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Get all .txt files in transcriptions directory
    text_paths = [os.path.join(transcriptions_dir, file) for file in os.listdir(transcriptions_dir) if file.endswith('.txt')]

    if not text_paths:
        print(f"No text files found in the directory {transcriptions_dir}.")
        return

    start_time = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as executor:
        for text_path in text_paths:
            executor.submit(translate_text, text_path, output_dir)
    end_time = time.perf_counter()
    print(f"Text translation completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
