# downloader/views.py
from django.shortcuts import render
from .forms import TikTokURLForm, TikTokUsernameForm, YouTubeURLForm, FormatSelectionForm
from .utils import download_single_video, download_all_videos_from_profile, list_video_formats, download_youtube_video
from .forms import FacebookURLForm
from .utils import download_facebook_video_with_ytdlp

def tiktok_download_a_video__view(request):
    message = ""
    if request.method == 'POST':
        form = TikTokURLForm(request.POST)
        if form.is_valid():
            video_url = form.cleaned_data['tiktok_url']
            message = download_single_video(video_url)
    else:
        form = TikTokURLForm()
    return render(request, 'download_tiktok_video.html', {'form': form, 'message': message})

def tiktok_download_profile_videos_view(request):
    message = ""
    if request.method == 'POST':
        form = TikTokUsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            message = download_all_videos_from_profile(username)
    else:
        form = TikTokUsernameForm()
    return render(request, 'download_tiktok_profile.html', {'form': form, 'message': message})

def youtube_downloader_view(request):
    formats = []
    message = ""
    if request.method == 'POST':
        form = YouTubeURLForm(request.POST)
        if form.is_valid():
            youtube_url = form.cleaned_data['youtube_url']
            formats = list_video_formats(youtube_url)
            request.session['youtube_url'] = youtube_url
    else:
        form = YouTubeURLForm()
    return render(request, 'youtube_downloader.html', {'form': form, 'formats': formats})

def download_facebook_video_view(request):
    message = ""
    if request.method == 'POST':
        form = FacebookURLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            message = download_facebook_video_with_ytdlp(url)
    else:
        form = FacebookURLForm()
    return render(request, 'download_facebook_video.html', {'form': form, 'message': message})
