import yt_dlp
import os

def download_all_videos_from_profile(username: str):
    """
    Downloads all videos from a specified TikTok user's profile.
    """
    profile_url = f"https://www.tiktok.com/@{username}"
    save_directory = os.path.expanduser(f"~/Downloads/{username}_videos")
    os.makedirs(save_directory, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(save_directory, '%(title)s.%(ext)s'),
        'format': 'best',
        'quiet': False,
        'merge_output_format': 'mp4',
        'noplaylist': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading all videos from profile: {profile_url}...")
            ydl.download([profile_url])
        print(f"All videos downloaded successfully to {save_directory}")
    except Exception as e:
        print(f"An error occurred while downloading videos from the profile: {e}")
