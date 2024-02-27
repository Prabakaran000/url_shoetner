from django.db import models

# urls_shortener/models.py
from django.db import models

class ShortenedURL(models.Model):
    original_url = models.URLField(unique=True)
    short_code = models.CharField(max_length=15, unique=True)

class URLClick(models.Model):
    shortened_url = models.ForeignKey(ShortenedURL, on_delete=models.CASCADE)
    click_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=50)