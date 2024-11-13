import yt_dlp
import os

def download_single_video(video_url: str):
    """
    Downloads a single TikTok video using the provided URL.
    """
    save_path = os.path.expanduser("~/Downloads/tiktok_video.mp4")
    
    ydl_opts = {
        'outtmpl': save_path,
        'format': 'best',
        'quiet': False,
        'merge_output_format': 'mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading TikTok video from URL: {video_url}...")
            ydl.download([video_url])
        print(f"Video downloaded successfully to {save_path}")
    except Exception as e:
        print(f"An error occurred while downloading the video: {e}")
