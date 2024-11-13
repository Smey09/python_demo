# downloader/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('tiktok_a_video/', views.tiktok_download_a_video__view, name='tiktok_a_video'),
    path('tiktok_a_profile/', views.tiktok_download_profile_videos_view, name='download_tiktok_profile'),
    path('youtube_downloader/', views.youtube_downloader_view, name='youtube_downloader'),
    path('facebook_downloader/', views.download_facebook_video_view, name='facebook_downloader'),
]
