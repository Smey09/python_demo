# downloader/utils.py
import yt_dlp
import os
import re
import subprocess
from urllib.parse import urlparse, parse_qs

def download_single_video(video_url: str):
    save_path = os.path.expanduser("~/Downloads/tiktok_video.mp4")
    ydl_opts = {
        'outtmpl': save_path,
        'format': 'best',
        'quiet': False,
        'merge_output_format': 'mp4',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return f"Video downloaded successfully to {save_path}"
    except Exception as e:
        return f"Error downloading video: {e}"

def download_all_videos_from_profile(username: str):
    profile_url = f"https://www.tiktok.com/@{username}"
    save_directory = os.path.expanduser(f"~/Downloads/{username}_videos")
    os.makedirs(save_directory, exist_ok=True)
    ydl_opts = {
        'outtmpl': os.path.join(save_directory, '%(title)s.%(ext)s'),
        'format': 'best',
        'merge_output_format': 'mp4',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([profile_url])
        return f"All videos downloaded successfully to {save_directory}"
    except Exception as e:
        return f"Error downloading videos from profile: {e}"

def list_video_formats(video_url):
    ydl_opts = {'format': 'all', 'noplaylist': True, 'quiet': True}
    formats_info = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get('formats', [])
            for f in formats:
                if f.get("vcodec") != "none" and f.get("ext") == "mp4" and f.get('filesize'):
                    formats_info.append({
                        "id": f['format_id'],
                        "resolution": f"{f.get('height')}p",
                        "size": f"{f['filesize'] / 1024 / 1024:.2f} MB",
                        "extension": f.get('ext')
                    })
        return formats_info
    except Exception as e:
        return f"Error retrieving video information: {e}"

def download_youtube_video(video_url, format_id):
    ydl_opts = {
        'format': format_id,
        'outtmpl': '~/Downloads/%(title)s.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return "Download completed successfully!"
    except Exception as e:
        return f"Error downloading video: {e}"

def extract_video_id(url):
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.split('/')
    for segment in path_segments:
        if segment.isdigit():
            return segment

    query_params = parse_qs(parsed_url.query)
    if 'v' in query_params and query_params['v'][0].isdigit():
        return query_params['v'][0]
    if 'video_id' in query_params and query_params['video_id'][0].isdigit():
        return query_params['video_id'][0]

    match = re.search(r'(\d{7,})', url)
    if match:
        return match.group(1)
    
    return None

def download_facebook_video_with_ytdlp(url):
    video_id = extract_video_id(url)
    if not video_id:
        return "Could not extract video ID from the URL."

    download_dir = os.path.expanduser("~/Downloads")
    save_path = os.path.join(download_dir, f"{video_id}.mp4")

    try:
        result = subprocess.run(["yt-dlp", url, "-o", save_path], check=True)
        if result.returncode == 0:
            return f"Downloaded video successfully to {save_path}"
        else:
            return "yt-dlp failed to download the video. Please check the URL or permissions."
    except FileNotFoundError:
        return "yt-dlp is not installed. Install it using 'pip install yt-dlp'."
    except subprocess.CalledProcessError as e:
        return f"An error occurred during download: {e}"