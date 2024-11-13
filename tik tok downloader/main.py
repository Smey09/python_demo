# Import the download_a_video, download_profile_videos, and youtube_downloader modules
import download_a_video
import download_profile_videos
import youtube_downloader

def main():
    print("Video Downloader")
    print("1. Download a single TikTok video by URL")
    print("2. Download all TikTok videos by user profile")
    print("3. YouTube downloader")
    choice = input("Enter your choice (1, 2, 3): ")

    if choice == "1":
        tiktok_url = input("Enter the TikTok video URL: ")
        download_a_video.download_single_video(tiktok_url)
    elif choice == "2":
        username = input("Enter the TikTok username: ")
        download_profile_videos.download_all_videos_from_profile(username)
    elif choice == "3":
        youtube_url = input("Enter the YouTube video URL: ")
        formats = youtube_downloader.list_video_formats(youtube_url)
        
        if formats:
            # Prompt the user to select a format ID after listing formats
            chosen_format_id = input("\nEnter the format ID to download: ")
            youtube_downloader.download_youtube_video(youtube_url, chosen_format_id)
        else:
            print("No downloadable formats found for this video.")
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
