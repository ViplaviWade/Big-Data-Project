import os
import sys
import time
import logging
import threading
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

# Configure Logging
logging.basicConfig(filename='download_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s', filemode='w')

# Define a mutex (Lock) for thread safety
mutex = threading.Lock()

# Define a semaphore to limit concurrent downloads to 5
semaphore = threading.Semaphore(5)

# Define a download directory
DOWNLOAD_DIR = 'downloads'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def read_video_urls(file_path):
    urls = []
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls

def download_video(url, thread_name):
    with semaphore:
        try:
            yt = YouTube(url)
            video_title = yt.title

            stream = yt.streams.filter(file_extension='mp4').first()
            file_path = os.path.join(DOWNLOAD_DIR, f"{yt.title}.mp4")

            stream.download(output_path=DOWNLOAD_DIR, filename=f"{yt.title}.mp4")

            with mutex:
                logging.info(f'"Timestamp": {time.strftime("%H:%M:%d %B %Y")},"URL":"{url}", "Download":True, "Thread/Process": "{thread_name}"')

            print(f"{thread_name} downloaded: {video_title}")
            
        except VideoUnavailable:
            with mutex:
                logging.error(f'"Timestamp": {time.strftime("%H:%M, %d %B %Y")}, "URL":"{url}", "Download":False, "Error":"VideoUnavailable", "Thread/Process": "{thread_name}"')
            print(f"{thread_name} failed to download: {url} (Video Unavailable)")

        except Exception as e:
            with mutex:
                logging.error(f'"Timestamp": {time.strftime("%H:%M, %d %B %Y")}, "URL":"{url}", "Download":False, "Error":"{str(e)}", "Thread/Process": "{thread_name}"')
            print(f"{thread_name} failed to download: {url} ({str(e)})")

def download_videos_serially(video_urls):
    start_time = time.perf_counter()
    
    for url in video_urls:
        download_video(url, "Serial")
    end_time = time.perf_counter()
    serial_time = end_time - start_time
    print(f"Serial download completed in {serial_time:.2f} seconds")
    return serial_time

def download_videos_parallely(video_urls):
    threads = []
    start_time = time.perf_counter()

    for i, url in enumerate(video_urls):
        thread_name = f"Thread-{i+1}"
        thread = threading.Thread(target=download_video, args=(url, thread_name))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

    end_time = time.perf_counter()
    parallel_time = end_time - start_time
    print(f"Parallel download completed in {parallel_time:.2f} seconds")
    return parallel_time

if __name__ == "__main__":
    with open("video_urls.txt", "r") as file:
        video_urls = [line.strip() for line in file.readlines()]

    print("Choose download method:")
    print("1. Serial Download")
    print("2. Parallel Download")

    choice = input("Enter 1 or 2: ")

    if choice == "1":
        download_videos_serially(video_urls)
    elif choice == "2":
        download_videos_parallely(video_urls)
    else:
        print("Invalid choice. Please enter 1 or 2.")
        sys.exit(1)