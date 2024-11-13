import subprocess
import os
import re
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    """
    Extract the video ID from various possible Facebook video URL structures.
    This function checks common patterns for video ID presence in the URL path or query parameters.
    """
    parsed_url = urlparse(url)
    
    # Check if the video ID is part of the path, e.g., /videos/{videoID}/
    path_segments = parsed_url.path.split('/')
    for segment in path_segments:
        if segment.isdigit():
            return segment
    
    # Check if the video ID is in query parameters
    query_params = parse_qs(parsed_url.query)
    if 'v' in query_params and query_params['v'][0].isdigit():
        return query_params['v'][0]
    
    # Check for Facebook's /watch/ pattern (e.g., /watch?v={videoID})
    if 'video_id' in query_params and query_params['video_id'][0].isdigit():
        return query_params['video_id'][0]
    
    # Attempt to match video ID using regex as a fallback
    match = re.search(r'(\d{7,})', url)  # Look for a sequence of 7+ digits
    
    if match:
        return match.group(1)
    
    # Return None if no valid video ID found
    return None

def download_facebook_video_with_ytdlp(url):
    """
    Download a Facebook video using yt-dlp and save it to ~/Downloads.
    The video will be saved as {videoID}.mp4 to ensure uniqueness.
    """
    try:
        # Extract video ID for unique naming
        video_id = extract_video_id(url)
        if not video_id:
            print("Could not extract video ID from the URL.")
            return

        # Define the save path in ~/Downloads with unique video ID
        download_dir = os.path.expanduser("~/Downloads")
        save_path = os.path.join(download_dir, f"{video_id}.mp4")

        # Attempt to download using yt-dlp
        print(f"Attempting to download video from {url} using yt-dlp...")
        result = subprocess.run(["yt-dlp", url, "-o", save_path], check=True)
        
        if result.returncode == 0:
            print(f"Downloaded video successfully to {save_path}")
        else:
            print("yt-dlp failed to download the video. Please check the URL or permissions.")

    except FileNotFoundError:
        print("yt-dlp is not installed. Install it using 'pip install yt-dlp'.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during download: {e}")

# Get user input for the Facebook video URL
facebook_video_url = input("Enter the Facebook video URL: ")
download_facebook_video_with_ytdlp(facebook_video_url)
