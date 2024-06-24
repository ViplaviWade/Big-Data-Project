import os
import time
import shutil
import moviepy.editor as mp
from concurrent.futures import ThreadPoolExecutor

DOWNLOAD_DIR = 'downloads'
RESULTS_DIR = 'extracted_audio'

# Function to clear the results directory
def clear_results_directory(directory):
    """Delete all files in the specified directory."""
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

def extract_audio(video_path, output_dir):
    try:
        video = mp.VideoFileClip(video_path)
        audio_path = os.path.join(output_dir, f"{os.path.basename(video_path).split('.')[0]}.mp3")
        video.audio.write_audiofile(audio_path)
        print(f"Audio extracted and saved to {audio_path}")
    except Exception as e:
        print(f"Failed to extract audio from {video_path}. Reason: {e}")

def main(video_paths):
    start_time = time.perf_counter()

    # Clear the results directory before processing new videos
    clear_results_directory(RESULTS_DIR)

    # Ensure the output directory exists
    os.makedirs(RESULTS_DIR, exist_ok=True)

    with ThreadPoolExecutor(max_workers=5) as executor:
        for video_path in video_paths:
            executor.submit(extract_audio, video_path, RESULTS_DIR)

    end_time = time.perf_counter()
    print(f"Audio extraction completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    video_files = [os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.mp4')]

    if video_files:
        main(video_files)
    else:
        print("No video files found in the downloads directory.")
