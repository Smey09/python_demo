import yt_dlp

def list_video_formats(video_url):
    """
    Lists available video formats for a given YouTube URL, displaying only MP4 formats with numbered entries.
    Skips rows where file size is unknown.
    """
    ydl_opts = {
        'format': 'all',
        'noplaylist': True,
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Fetch video information
            info = ydl.extract_info(video_url, download=False)
            
            # Print basic video info
            print("\nVideo Title:", info.get("title", "Unknown"))
            print("Uploader:", info.get("uploader", "Unknown"))
            print("Available formats:", len(info.get('formats', [])))
            
            formats = info.get('formats', [])
            
            if not formats:
                print("No formats available for this video.")
                return []
            
            # Display available formats
            print("\nAvailable MP4 video formats (with known file size):")
            print("{:<5} {:<5} {:<10} {:<15} {:<10}".format("No", "ID", "Resolution", "File Size", "Extension"))
            print("-" * 50)
            
            count = 1
            for f in formats:
                if f.get("vcodec") != "none" and f.get("ext") == "mp4":
                    filesize = f.get('filesize')
                    
                    # Skip this row if filesize is unknown
                    if not filesize:
                        continue
                    
                    format_id = f['format_id']
                    height = f.get('height')
                    resolution = f"{height}p" if height else "N/A"
                    filesize_str = f"{filesize / 1024 / 1024:.2f} MB"  # Convert to MB
                    ext = f.get('ext', 'N/A')
                    
                    # Display format information with file size
                    print(f"{count:<5} {format_id:<5} {resolution:<10} {filesize_str:<15} {ext:<10}")
                    count += 1

            return formats

        except Exception as e:
            print(f"An error occurred while retrieving video information: {e}")
            return []

def download_youtube_video(video_url, format_id):
    """
    Downloads a YouTube video in the specified format.
    """
    ydl_opts = {
        'format': format_id,
        'outtmpl': '~/Downloads/%(title)s.%(ext)s',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\nDownloading video in format {format_id} from URL: {video_url}")
            ydl.download([video_url])
            print("Download completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
