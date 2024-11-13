# downloader/forms.py
from django import forms

class TikTokURLForm(forms.Form):
    tiktok_url = forms.URLField(label='TikTok Video URL')

class TikTokUsernameForm(forms.Form):
    username = forms.CharField(label='TikTok Username')

class YouTubeURLForm(forms.Form):
    youtube_url = forms.URLField(label='YouTube Video URL')

class FormatSelectionForm(forms.Form):
    format_id = forms.CharField(label='Format ID')

class FacebookURLForm(forms.Form):
    url = forms.URLField(label='Facebook Video URL',)

