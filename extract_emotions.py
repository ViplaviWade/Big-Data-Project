import os
import time
import json
import text2emotion as te
from concurrent.futures import ThreadPoolExecutor

def extract_emotions(text_path, output_dir):
    try:
        with open(text_path, "r") as file:
            text = file.read()
        
        # Extract emotions using the text2emotion library
        emotions = te.get_emotion(text)
        
        # Create the path for saving the extracted emotions
        filename = os.path.basename(text_path).split('.')[0]
        emotions_path = os.path.join(output_dir, f"{filename}_emotions.json")
        
        # Write the extracted emotions to a JSON file
        with open(emotions_path, "w") as file:
            json.dump(emotions, file)
        
        print(f"Emotions extracted and saved to {emotions_path}")
    except Exception as e:
        print(f"Error extracting emotions from {text_path}: {e}")

def main():
    transcriptions_dir = "transcribe_audio2text"  # Directory containing text files for analysis
    output_dir = "extracted_emotions"  # New directory to save extracted emotions
    
    if not os.path.exists(transcriptions_dir):
        print(f"The directory {transcriptions_dir} does not exist.")
        return

    # Create the output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Get all .txt files in the transcriptions directory
    text_paths = [os.path.join(transcriptions_dir, file) for file in os.listdir(transcriptions_dir) if file.endswith('.txt')]

    if not text_paths:
        print(f"No text files found in the directory {transcriptions_dir}.")
        return

    start_time = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as executor:
        for text_path in text_paths:
            # Submit tasks to the ThreadPoolExecutor
            executor.submit(extract_emotions, text_path, output_dir)
    end_time = time.perf_counter()
    print(f"Emotions extraction completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
