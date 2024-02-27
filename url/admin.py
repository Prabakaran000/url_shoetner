from django.contrib import admin
from . models import ShortenedURL, URLClick

admin.site.register(ShortenedURL)
admin.site.register(URLClick)
