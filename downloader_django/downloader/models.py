# downloader/models.py
from django.db import models

class Video(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=200)
    download_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
