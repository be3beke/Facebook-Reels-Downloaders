import os
import sys

# We check if yt-dlp is available in the WASM environment
try:
    import yt_dlp
except ImportError:
    print("Error: yt_dlp module not found in WASM environment.")
    sys.exit(1)

def run_wasmer_download():
    # In Wasmer, we usually mount the current directory as /mnt
    base_path = "/mnt" 
    links_file = os.path.join(base_path, "reels.txt")
    cookies_file = os.path.join(base_path, "facebook_cookies.txt")
    archive_file = os.path.join(base_path, "history.txt")

    if not os.path.exists(links_file):
        print(f"File not found: {links_file}")
        return

    with open(links_file, 'r') as f:
        links = [line.strip() for line in f if line.strip()]

    # Batch selection
    start = 0 # Defaulting for automation
    end = 20
    batch = links[start:end]

    ydl_opts = {
        # 'best' ensures we don't need external FFmpeg merging
        'format': 'best[height<=1080][ext=mp4]/best',
        'outtmpl': '/mnt/downloads/%(upload_date)s_%(id)s.%(ext)s',
        'cookiefile': cookies_file if os.path.exists(cookies_file) else None,
        'download_archive': archive_file,
        'socket_timeout': 120,
        'retries': 10,
        'quiet': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(batch)

if __name__ == "__main__":
    run_wasmer_download()
