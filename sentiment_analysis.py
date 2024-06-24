import os
import time
import json
from textblob import TextBlob
from concurrent.futures import ThreadPoolExecutor

def analyze_sentiment(text_path, output_dir):
    with open(text_path, "r") as file:
        text = file.read()
    
    blob = TextBlob(text)
    sentiment = {
        "polarity": blob.sentiment.polarity,
        "subjectivity": blob.sentiment.subjectivity
    }
    sentiment_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(text_path))[0]}_sentiment.json")
    with open(sentiment_path, "w") as file:
        json.dump(sentiment, file)
    print(f"Sentiment analysis saved to {sentiment_path}")

def main(text_paths):
    start_time = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as executor:
        for text_path in text_paths:
            output_dir = os.path.join("sentiment_analysis", os.path.splitext(os.path.basename(text_path))[0])
            os.makedirs(output_dir, exist_ok=True)
            executor.submit(analyze_sentiment, text_path, output_dir)
    end_time = time.perf_counter()
    print(f"Sentiment analysis completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    transcription_folder = "transcribe_audio2text"
    text_paths = [os.path.join(transcription_folder, file) for file in os.listdir(transcription_folder) if file.endswith('.txt')]
    main(text_paths)
